"""Three-arm runner.

  full        : prompt + full styled prior session   (upper bound)
  compressed  : prompt + neutral summary of session  (baseline to beat)
  primed      : compressed + retrieved primer(s) injected

Reports the two metric heads separately, plus per-style-check breakdown, plus a
crude cost proxy (prompt tokens), so you can read the result COST-ADJUSTED.
"""
import json
import torch

from config import Config
from model import HookedLM
from primers import PrimerBank, extract_primer
from compress import compress_context
from metrics import content_score, conformance_score
import tasks


def build_prompt(instruction, context):
    return (f"{context}\n\nNow solve this, following the same conventions:\n"
            f"{instruction}\n\nReturn only the function in a ```python block.")


def main():
    cfg = Config()
    lm = HookedLM(cfg)
    bank = PrimerBank(cfg.bank_path)

    # 1) Build ONE working-mode primer from the contrastive pairs and store it.
    print("Extracting primer ...")
    direction = extract_primer(lm, tasks.extraction_pairs(), cfg.extract_layer)
    bank.save("house_style", direction, cfg.inject_layers[0],
              descriptor="house style python type hints docstring valueerror snake_case",
              alpha=cfg.alpha)

    # 2) Compress the prior session ONCE (shared by compressed + primed arms).
    print("Compressing prior session ...")
    summary = compress_context(lm, tasks.PRIOR_SESSION, cfg.compress_ratio)

    rows = []
    for t in tasks.TASKS:
        contexts = {
            "full": tasks.PRIOR_SESSION,
            "compressed": summary,
            "primed": summary,  # same context, primer added at generation
        }
        pids = bank.retrieve(t["descriptor"], k=1)  # the selection step
        for arm, ctx in contexts.items():
            prompt = build_prompt(t["instruction"], ctx)
            ids = lm.render(None, prompt)
            primers = bank.as_injection(pids, cfg.alpha) if arm == "primed" else None
            gen = lm.generate(ids, primers=primers)
            c = content_score(gen, t["tests"])
            conf, breakdown = conformance_score(gen)
            rows.append(dict(task=t["id"], arm=arm, content=c, conformance=conf,
                             prompt_tokens=int(ids.shape[1]), checks=breakdown))
            print(f"[{t['id']:>22}] {arm:>10} | content={c:.0f} "
                  f"conformance={conf:.2f} tokens={ids.shape[1]}")

    # 3) Aggregate per arm.
    print("\n=== Aggregate (mean over tasks) ===")
    summary_rows = {}
    for arm in ("full", "compressed", "primed"):
        sub = [r for r in rows if r["arm"] == arm]
        agg = dict(
            content=sum(r["content"] for r in sub) / len(sub),
            conformance=sum(r["conformance"] for r in sub) / len(sub),
            prompt_tokens=sum(r["prompt_tokens"] for r in sub) / len(sub),
        )
        summary_rows[arm] = agg
        print(f"{arm:>10} | content={agg['content']:.2f} "
              f"conformance={agg['conformance']:.2f} "
              f"avg_prompt_tokens={agg['prompt_tokens']:.0f}")

    with open(cfg.results_path, "w") as f:
        json.dump(dict(per_run=rows, aggregate=summary_rows,
                       config=cfg.__dict__), f, indent=2)
    print(f"\nWrote {cfg.results_path}")
    print("Read it as: does 'primed' lift conformance toward 'full' while "
          "keeping content ~flat and tokens ~= 'compressed'?")


if __name__ == "__main__":
    main()
