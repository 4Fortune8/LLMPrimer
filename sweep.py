"""Hyperparameter sweep for the primer: alpha x inject-layer, scored on the VAL
split (never train, never test). For each candidate we extract a primer AT that
layer and inject it AT that layer with that alpha, then measure how far it lifts
conformance over the `compressed` baseline and how much content it costs.

Selection rule (per domain and overall): maximise conformance gain over
compressed subject to content not dropping by more than cfg.content_tolerance.
This is the proper ML hygiene step — pick on val, then run.py reports on test.

Writes sweep.json (full grid) and prints a table. A matplotlib plot is emitted
only if the library is available; otherwise it is skipped silently.
"""
import json

from config import Config
from model import HookedLM
from primers import extract_primer
from compress import compress_context
from metrics import score_content, score_conformance
import suite
from run import build_prompt


def _eval_split(lm, domain, summary, split, primers):
    """Mean content/conformance over `split` tasks for one arm (primers or None)."""
    tasks = suite.tasks_for(domain, split)
    cs, fs = [], []
    for t in tasks:
        ids = lm.render(None, build_prompt(domain, t["instruction"], summary))
        gen = lm.generate(ids, primers=primers)
        cs.append(score_content(domain, gen, t["content"]))
        fs.append(score_conformance(domain, gen)[0])
    n = max(len(tasks), 1)
    return sum(cs) / n, sum(fs) / n


def main():
    cfg = Config()
    lm = HookedLM(cfg)
    grid = []          # every (domain, layer, alpha) cell
    selections = {}    # best cell per domain

    for domain in cfg.domains:
        info = suite.DOMAINS[domain]
        print(f"\n###### SWEEP DOMAIN: {domain} ######")
        summary = compress_context(lm, info["session"], cfg.compress_ratio)
        pairs = suite.extraction_pairs(domain)

        base_c, base_f = _eval_split(lm, domain, summary, "val", None)
        print(f"  compressed baseline (val): content={base_c:.2f} "
              f"conformance={base_f:.2f}")

        best = None
        for layer in cfg.sweep_layers:
            direction = extract_primer(lm, pairs, layer)
            for alpha in cfg.sweep_alphas:
                primers = [(layer, direction, float(alpha))]
                c, fconf = _eval_split(lm, domain, summary, "val", primers)
                cell = dict(domain=domain, layer=layer, alpha=float(alpha),
                            content=c, conformance=fconf,
                            conf_gain=fconf - base_f, content_delta=c - base_c)
                grid.append(cell)
                ok = cell["content_delta"] >= -cfg.content_tolerance
                flag = "" if ok else "  (content drop too big)"
                print(f"  layer={layer:>2} alpha={alpha:>4.1f} | "
                      f"content={c:.2f} ({cell['content_delta']:+.2f}) "
                      f"conformance={fconf:.2f} (gain {cell['conf_gain']:+.2f}){flag}")
                if ok and (best is None or cell["conf_gain"] > best["conf_gain"]):
                    best = cell
        selections[domain] = best
        if best:
            print(f"  -> selected layer={best['layer']} alpha={best['alpha']} "
                  f"(conf gain {best['conf_gain']:+.2f}, content "
                  f"{best['content_delta']:+.2f})")
        else:
            print("  -> no cell kept content within tolerance")

    with open("sweep.json", "w") as f:
        json.dump(dict(grid=grid, selections=selections,
                       config=cfg.__dict__), f, indent=2)
    print("\nWrote sweep.json")
    print("Selected (per domain) layer/alpha:")
    for d, b in selections.items():
        if b:
            print(f"  {d:>8}: layer={b['layer']} alpha={b['alpha']} "
                  f"conf_gain={b['conf_gain']:+.2f}")
    _maybe_plot(grid)


def _maybe_plot(grid):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return
    domains = sorted({c["domain"] for c in grid})
    fig, axes = plt.subplots(1, len(domains), figsize=(5 * len(domains), 4),
                             squeeze=False)
    for ax, domain in zip(axes[0], domains):
        cells = [c for c in grid if c["domain"] == domain]
        for layer in sorted({c["layer"] for c in cells}):
            pts = sorted((c for c in cells if c["layer"] == layer),
                         key=lambda c: c["alpha"])
            ax.plot([c["alpha"] for c in pts],
                    [c["conf_gain"] for c in pts], marker="o", label=f"L{layer}")
        ax.axhline(0, color="grey", lw=0.5)
        ax.set_title(domain)
        ax.set_xlabel("alpha")
        ax.set_ylabel("conformance gain over compressed")
        ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig("sweep.png", dpi=120)
    print("Wrote sweep.png")


if __name__ == "__main__":
    main()
