"""Multi-domain, split-aware runner for the priming experiment.

For each DOMAIN (coding / math / writing) it builds ONE working-mode primer from
that domain's TRAIN tasks, compresses that domain's styled prior session once,
then evaluates four arms on the chosen split (default: held-out TEST):

  full        : prompt + full styled prior session            (upper bound)
  compressed  : prompt + neutral summary of session           (cheap baseline)
  style_text  : compressed + the short contract text re-pasted (cheap TEXT rival
                the primer must justify itself against; costs extra tokens)
  primed      : compressed + the domain primer injected        (our method)

Two orthogonal heads are scored per task: content (facts) and conformance
(working mode). Generations and per-check breakdowns are saved so the run is
actually inspectable (results.json + results_readable.md).
"""
import json
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

ARMS = ("full", "compressed", "style_text", "primed")


def build_prompt(domain, instruction, context):
    return (f"{context}\n\nNow respond, following the same conventions:\n"
            f"{instruction}\n\n{SUFFIX[domain]}")


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


def main():
    cfg = Config()
    lm = HookedLM(cfg)
    bank = PrimerBank(cfg.bank_path)
    points = _operating_points(cfg)
    rows = []

    for domain in cfg.domains:
        info = suite.DOMAINS[domain]
        layer, alpha = points[domain]
        print(f"\n###### DOMAIN: {domain} (layer={layer} alpha={alpha}) ######")

        # 1) build the domain primer from TRAIN tasks only (no leak into val/test).
        #    Extract AND inject at the val-selected layer (invariant #4: same regime).
        print("  extracting primer ...")
        direction = extract_primer(lm, suite.extraction_pairs(domain), layer)
        bank.save(domain, direction, layer,
                  descriptor=info["descriptor"], alpha=alpha)

        # 2) compress the styled prior session ONCE (shared by compressed/primed)
        print("  compressing prior session ...")
        summary = compress_context(lm, info["session"], cfg.compress_ratio)

        contexts = {
            "full": info["session"],
            "compressed": summary,
            "style_text": info["contract"] + "\n" + summary,
            "primed": summary,
        }
        primers = bank.as_injection([domain], alpha)

        for t in suite.tasks_for(domain, cfg.eval_split):
            for arm in ARMS:
                prompt = build_prompt(domain, t["instruction"], contexts[arm])
                ids = lm.render(None, prompt)
                inj = primers if arm == "primed" else None
                gen = lm.generate(ids, primers=inj)
                c = score_content(domain, gen, t["content"])
                conf, breakdown = score_conformance(domain, gen)
                rows.append(dict(domain=domain, task=t["id"], arm=arm,
                                 content=c, conformance=conf,
                                 prompt_tokens=int(ids.shape[1]),
                                 checks=breakdown, generation=gen))
                failed = [k for k, v in breakdown.items() if not v]
                print(f"  [{t['id']:>20}] {arm:>10} | content={c:.2f} "
                      f"conformance={conf:.2f} tokens={ids.shape[1]} "
                      f"| failed={failed or '-'}")

    # 3) aggregate per (domain, arm) and overall per arm
    def agg(sub):
        n = len(sub)
        return dict(content=sum(r["content"] for r in sub) / n,
                    conformance=sum(r["conformance"] for r in sub) / n,
                    prompt_tokens=sum(r["prompt_tokens"] for r in sub) / n, n=n)

    aggregate = {"by_domain": {}, "overall": {}}
    print("\n=== Aggregate by domain ===")
    for domain in cfg.domains:
        aggregate["by_domain"][domain] = {}
        for arm in ARMS:
            sub = [r for r in rows if r["domain"] == domain and r["arm"] == arm]
            if not sub:
                continue
            a = agg(sub)
            aggregate["by_domain"][domain][arm] = a
            print(f"  {domain:>8} {arm:>10} | content={a['content']:.2f} "
                  f"conformance={a['conformance']:.2f} tokens={a['prompt_tokens']:.0f}")

    print("\n=== Overall (mean over all tasks) ===")
    for arm in ARMS:
        sub = [r for r in rows if r["arm"] == arm]
        a = agg(sub)
        aggregate["overall"][arm] = a
        print(f"  {arm:>10} | content={a['content']:.2f} "
              f"conformance={a['conformance']:.2f} avg_tokens={a['prompt_tokens']:.0f}")

    with open(cfg.results_path, "w") as f:
        json.dump(dict(per_run=rows, aggregate=aggregate, config=cfg.__dict__),
                  f, indent=2)
    _write_readable(rows, aggregate, cfg)
    print(f"\nWrote {cfg.results_path} and results_readable.md")
    print("Read it as: does 'primed' lift conformance toward 'full' (and beat "
          "'style_text' at lower tokens) while content stays ~flat?")


def _write_readable(rows, aggregate, cfg):
    with open("results_readable.md", "w") as f:
        f.write("# Primer harness run (multi-domain, split="
                f"{cfg.eval_split})\n\n## Overall\n\n")
        f.write("| arm | content | conformance | avg_tokens |\n|---|---|---|---|\n")
        for arm in ARMS:
            a = aggregate["overall"][arm]
            f.write(f"| {arm} | {a['content']:.2f} | {a['conformance']:.2f} "
                    f"| {a['prompt_tokens']:.0f} |\n")
        for domain in cfg.domains:
            f.write(f"\n## Domain: {domain}\n\n")
            f.write("| arm | content | conformance | avg_tokens |\n|---|---|---|---|\n")
            for arm in ARMS:
                a = aggregate["by_domain"][domain].get(arm)
                if a:
                    f.write(f"| {arm} | {a['content']:.2f} | {a['conformance']:.2f} "
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
