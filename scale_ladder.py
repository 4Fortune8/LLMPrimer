"""Scale ladder (Phase C): run the IDENTICAL harness across model sizes to test
the central question of the first-pass null — is the limitation model size?

For each model in cfg.model_ladder it builds a per-model Config (swapping
model_name / load_in_4bit), loads the model, runs run.evaluate(), and records the
two quantities that the "limitation is size" hypothesis predicts should grow with
parameters:

  primer_effect = primed.conformance - compressed.conformance   (does the primer
                  recover regime conditioning at all?)
  rival_gap     = primed.conformance - style_text.conformance    (does it beat the
                  cheap re-pasted-text rival it must justify itself against?)

Both are computed on the GATED overall (only domains whose `full` arm clears the
capability gate count as evidence; INVARIANT #3). Per-model results are saved as
results_<tag>.json / results_readable_<tag>.md; the ladder summary goes to
ladder.json (+ ladder.png if matplotlib is present).

NOTE on hyperparameters: operating points come from sweep.json if present (shared
across models) else config defaults. For a rigorous ladder, sweep each model on
val first; this runner uses whatever sweep.json provides and falls back cleanly.
"""
import dataclasses
import gc
import json
import re

from config import Config
from model import HookedLM
import run as runner


def _tag(model_name):
    return model_name.split("/")[-1]


def _params_b(model_name):
    """Approximate parameter count (billions) parsed from the model name."""
    m = re.search(r"(\d+(?:\.\d+)?)\s*[bB]\b", model_name)
    return float(m.group(1)) if m else float("nan")


def _free(lm):
    try:
        import torch
        del lm
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception:
        gc.collect()


def main():
    base = Config()
    ladder = []

    for spec in base.model_ladder:
        cfg = dataclasses.replace(base, model_name=spec["model_name"],
                                  load_in_4bit=spec.get("load_in_4bit", False))
        tag = _tag(cfg.model_name)
        print(f"\n########## SCALE LADDER: {tag} "
              f"(~{_params_b(cfg.model_name)}B, 4bit={cfg.load_in_4bit}) ##########")
        try:
            lm = HookedLM(cfg)
        except Exception as e:  # OOM / download / gated model -> skip, keep going
            print(f"  !! could not load {tag}: {e}")
            ladder.append(dict(tag=tag, params_b=_params_b(cfg.model_name),
                               error=str(e)))
            continue

        rows, aggregate = runner.evaluate(cfg, lm)

        with open(f"results_{tag}.json", "w") as f:
            json.dump(dict(per_run=rows, aggregate=aggregate,
                           config=cfg.__dict__), f, indent=2)
        runner._write_readable(rows, aggregate, cfg,
                               path=f"results_readable_{tag}.md")

        gov = aggregate.get("overall_gated", {})
        comp = gov.get("compressed")
        style = gov.get("style_text")
        primed = gov.get("primed")
        full = aggregate["overall"].get("full")
        row = dict(tag=tag, params_b=_params_b(cfg.model_name),
                   gated_domains=aggregate.get("gated_domains", []),
                   full_conformance=full["conformance"] if full else None)
        if comp and style and primed:
            row.update(
                compressed_conf=comp["conformance"],
                style_text_conf=style["conformance"],
                primed_conf=primed["conformance"],
                primer_effect=primed["conformance"] - comp["conformance"],
                rival_gap=primed["conformance"] - style["conformance"],
                tokens_primed=primed["prompt_tokens"],
                tokens_style_text=style["prompt_tokens"])
        else:
            row["note"] = "no domain cleared the capability gate"
        ladder.append(row)
        print(f"  -> {tag}: primer_effect="
              f"{row.get('primer_effect', float('nan')):.2f} "
              f"rival_gap={row.get('rival_gap', float('nan')):.2f} "
              f"(gated={row['gated_domains']})")

        _free(lm)

    with open("ladder.json", "w") as f:
        json.dump(dict(ladder=ladder, config=base.__dict__), f, indent=2)

    print("\n=== SCALE LADDER SUMMARY ===")
    print(f"{'model':>22} {'params':>7} {'primer_eff':>11} {'rival_gap':>10} "
          f"{'full_conf':>9}  gated")
    for r in ladder:
        if "error" in r:
            print(f"{r['tag']:>22} {r['params_b']:>6.1f}B  (load failed)")
            continue
        pe = r.get("primer_effect")
        rg = r.get("rival_gap")
        fc = r.get("full_conformance")
        print(f"{r['tag']:>22} {r['params_b']:>6.1f}B "
              f"{(f'{pe:+.2f}' if pe is not None else '   n/a'):>11} "
              f"{(f'{rg:+.2f}' if rg is not None else '  n/a'):>10} "
              f"{(f'{fc:.2f}' if fc is not None else ' n/a'):>9}  {r['gated_domains']}")
    print("\nHypothesis 'limitation is size' predicts primer_effect rises and "
          "rival_gap crosses 0 (primer overtakes re-pasting) as params grow.")
    _maybe_plot(ladder)
    print("Wrote ladder.json")


def _maybe_plot(ladder):
    pts = [r for r in ladder if r.get("primer_effect") is not None]
    if len(pts) < 2:
        return
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return
    pts.sort(key=lambda r: r["params_b"])
    xs = [r["params_b"] for r in pts]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(xs, [r["primer_effect"] for r in pts], marker="o",
            label="primer_effect (primed - compressed)")
    ax.plot(xs, [r["rival_gap"] for r in pts], marker="s",
            label="rival_gap (primed - style_text)")
    ax.axhline(0, color="grey", lw=0.5)
    ax.set_xlabel("model size (billions of parameters)")
    ax.set_ylabel("conformance delta (gated overall)")
    ax.set_title("Primer effect and rival gap vs model scale")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig("ladder.png", dpi=120)
    print("Wrote ladder.png")


if __name__ == "__main__":
    main()
