# AGENTS.md — Context packet for Primer-Bank + Compression Harness

> Read this fully before editing. This project is a research experiment; many
> "obvious improvements" silently invalidate the result. The INVARIANTS section
> is as important as the code. Rename/symlink this to `CLAUDE.md` if needed.

---

## 1. Mission (don't drift from this)
Test whether, **after neutral context compression**, re-injecting a small
"working-mode" steering vector (a *primer*) into a fresh generation recovers the
**behavioural conformance** that compression diluted — **without** restoring
factual content and at **near-zero added cost** (a few KB of storage, one vector
add per forward pass, no extra prompt tokens).

This is NOT trying to beat a full-context model. The bar is **cost-adjusted**:
match the cheap `compressed` baseline on cost while moving conformance toward the
`full` upper bound.

## 2. Hypothesis & win condition (optimise for THIS)
A primer carries low-rank *regime* information (style, conventions, working mode),
not high-rank *content* (specific code, values). Compression tends to keep facts
and wash out diffuse regime conditioning. So:

- **Predicted:** `primed.conformance` > `compressed.conformance`, approaching
  `full.conformance`; `primed.content` ≈ `compressed.content`; `primed` prompt
  tokens ≈ `compressed` prompt tokens.
- **Null/failure (report honestly):** primer also fails to move conformance, OR
  it moves conformance only by wrecking content/fluency, OR a plain re-pasted
  style string (the cheap rival baseline) does just as well for similar cost.

## 3. Prior art — cite these, do NOT reinvent, frame novelty against them
| concept | what it is | id |
|---|---|---|
| Function Vectors | mean-diff activation that triggers a task in new contexts | Todd et al. 2023 (arXiv 2310.15213) |
| Task Vectors | ICL compresses a task into a vector ≈ one demonstration's worth | Hendel et al. 2023 (2310.15916) |
| ActAdd | steering by adding a contrastive activation difference | Turner et al. 2023 (2308.10248) |
| Coconut | reason in latent space by feeding hidden state back as input | Hao et al. 2024 (2412.06769) |
| ASC | steering vector to compress chains-of-thought | 2507.04742 |
| COS-Steering | SAE-compressed steering basis + lightweight input-conditioned selector | OpenReview vzXyVNCGAL |
| Learned Task Vectors | trained primers beat extracted ones by ~9.2% avg | 2509.24169 |
| "Steerable but Not Decodable" | difficulty hierarchy: easy tasks recover fully, HARD tasks ~zero | 2604.02608 |

**Our defensible novelty = the *division of labor* (content-compression for facts
+ cheap primer reinjection for working mode) measured with TWO ORTHOGONAL HEADS.**
Frame any writeup as that. Anything broader will be (correctly) called derivative.

## 4. Repo map
- `config.py` — single source of truth: model, `inject_layers`, `alpha`,
  `extract_layer`, `compress_ratio`, generation, seed. Edit here, not inline.
- `model.py` — `HookedLM`: `render()` (chat template), `last_token_residual()`
  (capture for extraction), `inject()` (context manager adding `alpha·vec` to a
  layer's residual for ALL positions), `generate()`.
- `primers.py` — `extract_primer()` (contrastive mean-diff, unit-normed) and
  `PrimerBank` (save/load/`retrieve`/`as_injection`). Retrieval is Jaccard on
  descriptors — intentionally a stub.
- `compress.py` — `compress_context()`, a neutral faithful summariser.
- `tasks.py` — `HOUSE_STYLE`, `PRIOR_SESSION`, `TASKS` (instruction + hidden
  tests), `extraction_pairs()`.
- `metrics.py` — `content_score()` (subprocess unit tests, pass@1) and
  `conformance_score()` (AST style checks → score + per-check breakdown).
- `run.py` — three-arm loop, aggregation, writes `results.json`.

## 5. INVARIANTS — violating these invalidates the experiment
1. **Never rig the compressor.** `compress.py` must stay a generic, faithful
   summariser. Do not special-case it to drop the house style. That is circular.
2. **Keep the two heads orthogonal.** Content tests = valid-input behaviour only.
   The style/error contract is scored ONLY by `conformance_score`. Do not add
   contract asserts (e.g. "raises ValueError") into `tests`.
3. **Tasks must be solvable by the base model.** Headroom must live in
   conformance, not raw capability (see difficulty-hierarchy result). If you add
   tasks, verify `full.content` ≈ 1.0 first; if it's low, the task is too hard.
4. **Extract/validate primers in the regime they run in.** Primers are used on
   *compressed* prompts; a primer extracted only from full-context activations may
   mismatch. At minimum re-tune `alpha` on compressed prompts.
5. **Few primers, different layers.** Summed vectors at one layer interfere. If
   adding multiple primers, spread across `inject_layers`, don't stack at one.
6. **Always run the demanded baselines:** zero-shot, `compressed`, `compressed +
   re-pasted short style text` (the cheap text rival the primer must beat), and
   `full` (upper bound). The text rival is the one reviewers will insist on.
7. **Report the sweep, not one point.** Effect peaks mid-stack; large `alpha`
   destroys fluency. Any headline number must come with an alpha×layer sweep.
8. **Determinism:** keep `temperature=0` (greedy) and the fixed `seed` for
   reported runs. Only sample for variance studies, and then report seeds.

## 6. Backlog (priority order)
1. `sweep.py` — loop `alpha ∈ {2,4,6,8,10,12}` × `layer ∈ mid-stack`, dump a
   table + simple plot of (conformance gain) vs (content delta) vs alpha.
2. Add the **re-pasted-style-text** arm to `run.py` (invariant #6).
3. `modal_app.py` — wrap `run.py` for `modal run` on a cloud T4 (see README).
4. Upgrade `PrimerBank.retrieve` to embedding cosine (sentence-transformers) and
   study the SELECTION layer — which primer for an unseen task. This is the most
   genuinely open research question; treat it as its own mini-experiment.
5. Extract primers from **compressed-regime** prompts (invariant #4); compare to
   full-regime extraction.
6. Add ≥2 more task families (different house styles) to test generalisation and
   primer COMPOSITION (apply two primers, different layers).
7. Add a second model (e.g. Llama-3.2-3B) to test cross-model robustness.
8. Variance: re-run with several seeds, report mean ± std (single runs are noisy).

## 7. How to verify a change (sanity heuristics)
- `python -m py_compile *.py` then `python run.py` should complete and write
  `results.json`.
- **Bug smells:** `conformance` all 0.0 → generated code failed to AST-parse
  (codegen or `extract_code` regex broke). `content` all 0.0 → tests or codegen
  broken, OR tasks too hard (check `full` arm). `primed` identical to
  `compressed` → injection not firing (check layer index in range, hook attached,
  alpha ≠ 0).
- Quick head test without a GPU: import `metrics`, score a known-good vs
  no-style string; expect content 1.0/1.0 and conformance ~1.0/0.25.

## 8. Environment facts
- Default model `Qwen/Qwen2.5-1.5B-Instruct`, fp16, fits a free T4 (16GB). 7-8B
  needs `load_in_4bit=True` + `bitsandbytes`.
- Free GPU: Lightning AI (~80 h/mo, VS-Code-like), Kaggle (~30 h/wk dual T4),
  Colab (resets packages, ~12h cap), Modal (per-second, free credits). Sessions
  die — checkpoint `primer_bank/` and `results.json` to persistent storage.
- On restricted networks model weights may not download; pre-cache the model.

## 9. Glossary
- **primer** — a stored steering vector encoding a working mode/regime.
- **content head** — functional correctness (facts survived).
- **conformance head** — house-style adherence (working mode survived).
- **arm** — one experimental condition: full / compressed / primed (+ rivals).
- **regime / working mode** — diffuse, low-rank behaviour (style, conventions)
  as opposed to high-rank problem-specific content.

## 10. Tone for any writeup
Small, clean, honest, cost-adjusted. Cite neighbours generously. Publish null
results if that's what the data says. Do not overclaim — a modest reproducible
effect is the win; a big claim that won't replicate is the failure mode.
