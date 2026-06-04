"""Multi-domain, split-aware runner for the priming experiment.

For each DOMAIN (coding / math / writing) it builds ONE working-mode primer from
that domain's TRAIN tasks, compresses that domain's styled prior session once,
then evaluates five arms on the chosen split (default: held-out TEST):

  zero_shot   : prompt with NO context                         (lower anchor)
  full        : prompt + full styled prior session             (upper bound)
  compressed  : prompt + neutral summary of session            (cheap baseline)
  style_text  : compressed + the short contract text re-pasted (cheap TEXT rival
                the primer must justify itself against; costs extra tokens)
  primed      : compressed + the domain primer injected         (our method)

Two orthogonal heads are scored per task: content (facts) and conformance
(working mode). The reported run is greedy/deterministic; set cfg.seeds and
cfg.eval_temperature>0 for a variance pass (mean +/- std). Generations and
per-check breakdowns are saved so the run is inspectable (results.json +
results_readable.md).
"""
import json
import math
import os

from config import Config
from model import HookedLM
from primers import PrimerBank, extract_primer
from compress import compress_context
from metrics import score_content, score_conformance
import suite

# Neutral instruction suffix per domain. It must NOT encode the working-mode
# contract (that has to come from context/primer/rival), or there is nothing for
# the primer to restore.
SUFFIX = {
    "coding": "Return only the function in a ```python block.",
    "math": "Give your solution.",
    "writing": "Write a short explanation.",
}

ARMS = ("zero_shot", "full", "compressed", "style_text", "primed")


def build_prompt(domain, instruction, context):
    return (f"{context}\n\nNow respond, following the same conventions:\n"
            f"{instruction}\n\n{SUFFIX[domain]}")


def bare_prompt(domain, instruction):
    """Zero-shot prompt: no context, no convention hint."""
    return f"{instruction}\n\n{SUFFIX[domain]}"


def extraction_pairs(cfg, domain, summary):
    """Contrastive (mode_on, mode_off) pairs from the TRAIN split.

    INVARIANT #4: extract the primer in the regime it is injected in.
      compressed -> (contract + summary + task) vs (summary + task): isolates the
                    working-mode direction on top of the compressed-prompt
                    distribution where the primer actually runs.
      contract   -> legacy (contract + task) vs (task), full-style activations.
    """
    contract = suite.DOMAINS[domain]["contract"]
    pairs = []
    for t in suite.tasks_for(domain, "train"):
        if cfg.extract_regime == "compressed":
            on = build_prompt(domain, t["instruction"], contract + "\n" + summary)
            off = build_prompt(domain, t["instruction"], summary)
        else:
            on = contract + "\n" + t["instruction"]
            off = t["instruction"]
        pairs.append((on, off))
    return pairs


def _operating_points(cfg):
    """Per-domain (layer, alpha) chosen by the val sweep. Falls back to the
    config defaults when sweep.json is absent or a domain was not selected, so
    the test report always uses hyperparameters picked on val (never on test)."""
    default = (cfg.extract_layer, cfg.alpha)
    points = {d: default for d in cfg.domains}
    if os.path.exists("sweep.json"):
        with open("sweep.json") as f:
            sel = json.load(f).get("selections", {})
        for d, best in sel.items():
            if best:
                points[d] = (int(best["layer"]), float(best["alpha"]))
    return points


def _mean_sd(xs):
    n = len(xs)
    m = sum(xs) / n
    if n < 2:
        return m, 0.0
    var = sum((x - m) ** 2 for x in xs) / (n - 1)
    return m, math.sqrt(var)


def _score_arm(lm, cfg, domain, ids, primers, content_spec):
    """Run all seeds for one (task, arm); return mean/sd of both heads plus the
    first seed's generation and conformance breakdown for inspection."""
    cs, fs = [], []
    first_gen, first_checks = None, None
    for s in cfg.seeds:
        gen = lm.generate(ids, primers=primers, seed=s,
                          temperature=cfg.eval_temperature)
        c = score_content(domain, gen, content_spec)
        conf, breakdown = score_conformance(domain, gen)
        cs.append(c)
        fs.append(conf)
        if first_gen is None:
            first_gen, first_checks = gen, breakdown
    cm, csd = _mean_sd(cs)
    fm, fsd = _mean_sd(fs)
    return dict(content=cm, content_sd=csd, conformance=fm, conformance_sd=fsd,
                generation=first_gen, checks=first_checks)


def evaluate(cfg, lm, bank=None, points=None, log=print):
    """Run the full multi-domain, multi-arm evaluation for one model.

    Returns (rows, aggregate). Reused by scale_ladder.py across model sizes."""
    bank = bank or PrimerBank(cfg.bank_path)
    points = points or _operating_points(cfg)
    rows = []

    for domain in cfg.domains:
        info = suite.DOMAINS[domain]
        layer, alpha = points[domain]
        log(f"\n###### DOMAIN: {domain} (layer={layer} alpha={alpha}) ######")

        # compress the styled prior session ONCE (shared by compressed/primed)
        log("  compressing prior session ...")
        summary = compress_context(lm, info["session"], cfg.compress_ratio)

        # build the domain primer from TRAIN tasks, in the injection regime.
        log("  extracting primer ...")
        direction = extract_primer(lm, extraction_pairs(cfg, domain, summary), layer)
        bank.save(domain, direction, layer,
                  descriptor=info["descriptor"], alpha=alpha)

        contexts = {
            "full": info["session"],
            "compressed": summary,
            "style_text": info["contract"] + "\n" + summary,
            "primed": summary,
        }
        primers = bank.as_injection([domain], alpha)

        for t in suite.tasks_for(domain, cfg.eval_split):
            for arm in ARMS:
                if arm == "zero_shot":
                    prompt = bare_prompt(domain, t["instruction"])
                else:
                    prompt = build_prompt(domain, t["instruction"], contexts[arm])
                ids = lm.render(None, prompt)
                inj = primers if arm == "primed" else None
                r = _score_arm(lm, cfg, domain, ids, inj, t["content"])
                r.update(dict(domain=domain, task=t["id"], arm=arm,
                              prompt_tokens=int(ids.shape[1])))
                rows.append(r)
                failed = [k for k, v in r["checks"].items() if not v]
                log(f"  [{t['id']:>20}] {arm:>10} | content={r['content']:.2f} "
                    f"conformance={r['conformance']:.2f} tokens={ids.shape[1]} "
                    f"| failed={failed or '-'}")

    aggregate = _aggregate(cfg, rows)
    return rows, aggregate


def _aggregate(cfg, rows):
    def agg(sub):
        n = len(sub)
        cm, csd = _mean_sd([r["content"] for r in sub])
        fm, fsd = _mean_sd([r["conformance"] for r in sub])
        return dict(content=cm, content_sd=csd,
                    conformance=fm, conformance_sd=fsd,
                    prompt_tokens=sum(r["prompt_tokens"] for r in sub) / n, n=n)

    aggregate = {"by_domain": {}, "overall": {}, "value": {}}
    for domain in cfg.domains:
        aggregate["by_domain"][domain] = {}
        for arm in ARMS:
            sub = [r for r in rows if r["domain"] == domain and r["arm"] == arm]
            if sub:
                aggregate["by_domain"][domain][arm] = agg(sub)
        # capability gate (INVARIANT #3 on the conformance head)
        full = aggregate["by_domain"][domain].get("full", {})
        full_conf = full.get("conformance", 0.0)
        aggregate["by_domain"][domain]["_gate"] = dict(
            full_conformance=full_conf,
            passes=full_conf >= cfg.capability_gate)
        aggregate["value"][domain] = _value(aggregate["by_domain"][domain])

    for arm in ARMS:
        sub = [r for r in rows if r["arm"] == arm]
        if sub:
            aggregate["overall"][arm] = agg(sub)

    # gated overall: primer evidence ONLY from domains that clear the gate.
    gated = [d for d in cfg.domains
             if aggregate["by_domain"][d]["_gate"]["passes"]]
    aggregate["gated_domains"] = gated
    if gated:
        gsub = [r for r in rows if r["domain"] in gated]
        aggregate["overall_gated"] = {
            arm: agg([r for r in gsub if r["arm"] == arm])
            for arm in ARMS if any(r["arm"] == arm for r in gsub)}
        aggregate["value"]["__gated_overall__"] = _value(
            aggregate["overall_gated"])
    return aggregate


def _value(arm_aggs):
    """Cost-adjusted verdict: does `primed` dominate the text rival `style_text`?

    A primer earns its keep only if it reaches the rival's conformance at fewer
    prompt tokens (the rival re-pastes the contract on every call; the primer is
    a one-time vector add). Reports deltas vs both compressed and style_text.
    """
    comp = arm_aggs.get("compressed")
    style = arm_aggs.get("style_text")
    primed = arm_aggs.get("primed")
    if not (comp and style and primed):
        return None
    d_conf_comp = primed["conformance"] - comp["conformance"]
    d_conf_style = primed["conformance"] - style["conformance"]
    d_tok_style = primed["prompt_tokens"] - style["prompt_tokens"]
    # Pareto verdict on (conformance up, tokens down) vs the rival.
    if d_conf_style >= -1e-9 and d_tok_style <= 1e-9:
        verdict = "primer dominates rival"
    elif d_conf_style <= 1e-9 and d_tok_style >= -1e-9:
        verdict = "rival dominates primer"
    else:
        verdict = "mixed (trade-off)"
    return dict(conf_gain_over_compressed=d_conf_comp,
                conf_vs_style_text=d_conf_style,
                tokens_vs_style_text=d_tok_style,
                verdict=verdict)


def main():
    cfg = Config()
    lm = HookedLM(cfg)
    rows, aggregate = evaluate(cfg, lm)

    print("\n=== Aggregate by domain ===")
    for domain in cfg.domains:
        gate = aggregate["by_domain"][domain]["_gate"]
        tag = "PASS" if gate["passes"] else "below-gate (capability-bound)"
        print(f"  -- {domain} (full conformance={gate['full_conformance']:.2f} "
              f"-> {tag}) --")
        for arm in ARMS:
            a = aggregate["by_domain"][domain].get(arm)
            if a:
                print(f"     {arm:>10} | content={a['content']:.2f} "
                      f"conformance={a['conformance']:.2f} "
                      f"tokens={a['prompt_tokens']:.0f}")

    print("\n=== Overall (mean over all tasks) ===")
    for arm in ARMS:
        a = aggregate["overall"].get(arm)
        if a:
            print(f"  {arm:>10} | content={a['content']:.2f} "
                  f"conformance={a['conformance']:.2f} "
                  f"avg_tokens={a['prompt_tokens']:.0f}")

    if aggregate.get("gated_domains"):
        print(f"\n=== Overall (gated: {aggregate['gated_domains']}) ===")
        for arm in ARMS:
            a = aggregate.get("overall_gated", {}).get(arm)
            if a:
                print(f"  {arm:>10} | content={a['content']:.2f} "
                      f"conformance={a['conformance']:.2f} "
                      f"avg_tokens={a['prompt_tokens']:.0f}")
        v = aggregate["value"].get("__gated_overall__")
        if v:
            print(f"  VALUE (gated): primed vs style_text "
                  f"conf {v['conf_vs_style_text']:+.2f}, "
                  f"tokens {v['tokens_vs_style_text']:+.0f} -> {v['verdict']}")
    else:
        print("\n(no domain cleared the capability gate; primer evidence is "
              "capability-bound at this model size)")

    with open(cfg.results_path, "w") as f:
        json.dump(dict(per_run=rows, aggregate=aggregate, config=cfg.__dict__),
                  f, indent=2)
    _write_readable(rows, aggregate, cfg)
    print(f"\nWrote {cfg.results_path} and results_readable.md")


def _write_readable(rows, aggregate, cfg, path="results_readable.md"):
    with open(path, "w") as f:
        f.write(f"# Primer harness run ({cfg.model_name}, split={cfg.eval_split}, "
                f"seeds={list(cfg.seeds)}, regime={cfg.extract_regime})\n\n")
        f.write("## Overall\n\n")
        f.write("| arm | content | conformance | avg_tokens |\n|---|---|---|---|\n")
        for arm in ARMS:
            a = aggregate["overall"].get(arm)
            if a:
                f.write(f"| {arm} | {a['content']:.2f} | {a['conformance']:.2f}"
                        f" +/-{a['conformance_sd']:.2f} | {a['prompt_tokens']:.0f} |\n")

        f.write("\n## Value (cost-adjusted: primer vs re-pasted text rival)\n\n")
        f.write("| scope | conf gain vs compressed | conf vs style_text | "
                "tokens vs style_text | verdict |\n|---|---|---|---|---|\n")
        for domain in cfg.domains:
            v = aggregate["value"].get(domain)
            gate = aggregate["by_domain"][domain]["_gate"]
            scope = domain + ("" if gate["passes"] else " (below gate)")
            if v:
                f.write(f"| {scope} | {v['conf_gain_over_compressed']:+.2f} | "
                        f"{v['conf_vs_style_text']:+.2f} | "
                        f"{v['tokens_vs_style_text']:+.0f} | {v['verdict']} |\n")
        v = aggregate["value"].get("__gated_overall__")
        if v:
            f.write(f"| **gated overall** | {v['conf_gain_over_compressed']:+.2f} | "
                    f"{v['conf_vs_style_text']:+.2f} | "
                    f"{v['tokens_vs_style_text']:+.0f} | {v['verdict']} |\n")

        for domain in cfg.domains:
            gate = aggregate["by_domain"][domain]["_gate"]
            tag = "PASS" if gate["passes"] else "BELOW GATE (capability-bound)"
            f.write(f"\n## Domain: {domain} "
                    f"(full conformance={gate['full_conformance']:.2f} -> {tag})\n\n")
            f.write("| arm | content | conformance | avg_tokens |\n|---|---|---|---|\n")
            for arm in ARMS:
                a = aggregate["by_domain"][domain].get(arm)
                if a:
                    f.write(f"| {arm} | {a['content']:.2f} | "
                            f"{a['conformance']:.2f} +/-{a['conformance_sd']:.2f} "
                            f"| {a['prompt_tokens']:.0f} |\n")
            for t in suite.tasks_for(domain, cfg.eval_split):
                f.write(f"\n### {t['id']}\n\n> {t['instruction']}\n")
                for arm in ARMS:
                    r = next((x for x in rows if x["domain"] == domain
                              and x["task"] == t["id"] and x["arm"] == arm), None)
                    if not r:
                        continue
                    marks = ", ".join(f"{k}={'PASS' if v else 'x'}"
                                      for k, v in r["checks"].items())
                    f.write(f"\n**{arm}** \u2014 content={r['content']:.2f} "
                            f"conformance={r['conformance']:.2f} ({marks})\n\n")
                    f.write("```\n" + r["generation"].strip() + "\n```\n")


if __name__ == "__main__":
    main()
