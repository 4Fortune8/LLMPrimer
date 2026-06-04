# Primer-Bank + Compression Harness

Tests one hypothesis: **after neutral context compression, re-injecting a small
"working-mode" primer recovers behavioural conformance that compression diluted,
while barely touching factual correctness, at near-zero added cost.**

Two metric heads are measured **separately**:

| head | question | how |
|---|---|---|
| `content` | did the facts survive? | run generated code against hidden unit tests (pass@1) |
| `conformance` | did the working mode survive? | AST checks for house style (naming, type hints, docstring, error contract) |

Three arms: `full` (full styled context, upper bound) -> `compressed` (neutral
summary, baseline) -> `primed` (compressed + retrieved primer injected), plus two
rivals that keep the result honest: `zero_shot` (no context, lower anchor) and
`style_text` (compressed + the short contract text re-pasted -- the cheap text
rival the primer must beat on cost).

The report is **capability-gated** (a domain only counts as evidence if its
`full` arm clears `cfg.capability_gate` conformance) and **cost-adjusted**: the
`value` table asks whether `primed` reaches the text rival's conformance at fewer
prompt tokens.

## What "success" looks like
`primed` lifts **conformance** toward `full` while **content** stays ~flat and
prompt tokens stay ~= `compressed`. That is a cost-adjusted win, which is the
correct bar here — you are NOT trying to beat the full-context arm.

## Files
- `config.py` — model, inject layers, alpha, compression ratio, splits, seeds,
  capability gate, the scale ladder (start here)
- `model.py` — HF model + residual-stream capture/inject hooks + generate
- `primers.py` — function-vector extraction + on-disk bank + retrieval
- `compress.py` — model-based summariser (the compressor)
- `suite.py` — multi-domain tasks (coding/math/writing) with train/val/test splits
- `metrics.py` — the two heads, dispatched per domain
- `run.py` — the five-arm experiment (one model); exposes `evaluate()`
- `sweep.py` — alpha × layer selection on the VAL split (pick here, report on test)
- `scale_ladder.py` — runs the identical harness across model sizes (the key
  experiment for "is the limitation model size?")

## Run
```bash
pip install -r requirements.txt
python sweep.py         # select alpha x layer on val -> sweep.json (optional)
python run.py           # five-arm test report -> results.json + results_readable.md
python scale_ladder.py  # 1.5B -> 3B -> 7B ladder -> ladder.json + ladder.png
```
Default model `Qwen/Qwen2.5-1.5B-Instruct` runs on a free T4 in fp16. For 7-8B,
set `load_in_4bit=True` in `config.py` and `pip install bitsandbytes`.

## Running it cheaply from VS Code on a laptop
You write/edit locally in VS Code; the GPU lives in the cloud. Three good routes,
cheapest first (free-tier figures as of 2026 — verify, they drift):

1. **Lightning AI Studio (best VS-Code-like free option).** Browser workspace
   that behaves like a real machine: git, venvs, pytest, SSH, VS Code extensions,
   persistent storage. Roughly **~80 GPU hours/month free**, T4-class. Closest to
   "a remote dev box" rather than a notebook.
2. **Modal (best laptop-native workflow).** Code stays in your local VS Code; you
   wrap `run.py` in a Modal function and `modal run` it — it ships to a cloud GPU,
   bills per second, free monthly credits, sub-5s cold start. Ideal once the
   harness is stable and you want repeatable sweeps. (See `modal_app.py` pattern
   below.)
3. **Kaggle Notebooks (most reliable free GPU).** ~30 hrs/week, dual T4s, torch
   preinstalled, more stable than Colab. Editor is a notebook; drive code from a
   single cell `!python run.py`. **Colab** free (T4, ~15–30 hrs/wk) also works but
   resets installed packages each session and disconnects at ~12 h.

Cheap paid if you outgrow free: **RunPod** (~$0.2/hr spot, SSH from VS Code
Remote-SSH — feels local) or **Vast.ai** (RTX 3090 from ~$0.07–0.2/hr). New RunPod
accounts usually get a few dollars of starting credit.

Practical: free sessions disconnect and kernels crash — checkpoint `primer_bank/`
and `results.json` to persistent storage early, and keep the model small while
iterating so a full pass is minutes, not hours.

### Running on Lightning AI from your laptop
`lightning_run.py` ships the source to a Studio, runs it on a GPU, and downloads
results. Credentials come from `.env` (`LIGHTNING_USER_ID`, `LIGHTNING_API_KEY`).
```bash
.venv/bin/python lightning_run.py --machine T4            # five-arm test report
.venv/bin/python lightning_run.py --machine T4 --sweep    # val alpha x layer sweep
.venv/bin/python lightning_run.py --machine T4 --ladder   # scale ladder
```
Set `HF_TOKEN` (or persist the HF cache to the Studio home) before a ladder run —
otherwise large 7B weight downloads dominate GPU time.

### Minimal Modal wrapper (optional)
```python
# modal_app.py  — run with:  modal run modal_app.py
import modal
img = (modal.Image.debian_slim()
       .pip_install("torch","transformers","accelerate"))
app = modal.App("primer-harness", image=img)

@app.function(gpu="T4", timeout=3600)
def go():
    import subprocess; subprocess.run(["python","run.py"], check=True)

@app.local_entrypoint()
def main():
    go.remote()
```
Mount this folder into the image (`.add_local_dir(".", "/root")`) so your local
edits ship up each run.

## Methodological cautions (these decide whether the result means anything)
1. **Don't rig the compressor.** `compress.py` uses a neutral faithful summariser.
   If you hand-write a summary that drops exactly what the primer restores, the
   result is circular. Let neutral compression lose the "how" on its own.
2. **Keep the heads orthogonal.** Content tests cover valid-input behaviour only;
   the style/error contract is scored solely by the conformance head. Don't add
   contract asserts back into the tests.
3. **Use tasks the model can already solve.** The function-vector literature shows
   primers recover a lot on easy tasks and ~nothing on hard ones. Headroom must be
   in conformance, not in raw capability.
4. **Extract/validate primers in the regime you'll run them in.** A primer built
   against full-context activations may not match the compressed activation
   distribution — extract from, or at least re-tune alpha on, compressed prompts.
5. **Sweep alpha and layer.** Effect peaks mid-stack; too-large alpha wrecks
   fluency. Report the sweep, not one lucky point.
6. **A few primers, different layers.** Summed vectors at one layer interfere.
7. **Baselines that will be demanded of you:** zero-shot; compressed; compressed +
   *re-pasting the short style text* (the cheap text-prompt rival the primer must
   justify itself against); and the `full` upper bound.
