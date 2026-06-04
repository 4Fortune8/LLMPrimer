"""Central configuration. Edit MODEL_NAME / LAYERS / ALPHA here."""
from dataclasses import dataclass, field


@dataclass
class Config:
    # A small instruct model that fits a free T4 (16GB) in fp16. Swap freely.
    #   Qwen/Qwen2.5-1.5B-Instruct   (very light, decent at code for size)
    #   meta-llama/Llama-3.2-3B-Instruct  (gated; needs HF login)
    #   Qwen/Qwen2.5-3B-Instruct     (heavier but fine on T4 in fp16/4bit)
    model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"
    dtype: str = "float16"          # "float16" on T4; "bfloat16" on A10/A100
    device: str = "cuda"            # "cuda" / "cpu" / "mps"
    load_in_4bit: bool = False      # set True (with bitsandbytes) for 7-8B on a T4

    # Primer injection. Function-vector / steering-vector literature finds the
    # effect peaks at an INTERMEDIATE layer (~middle of the stack). Inject a FEW
    # primers at DIFFERENT layers rather than stacking them at one — summed
    # vectors at a single layer interfere.
    #
    # SCALE NOTE: layer indices are resolved as FRACTIONS of the model's depth
    # (see *_layer_fracs below) so "mid-stack" tracks the architecture. A fixed
    # absolute layer (e.g. 8) is mid-stack on a 28-layer 1.5B but bottom-stack on
    # a 64-layer 32B — which would inject the primer in the wrong region. The
    # absolute fields below are legacy fallbacks only.
    inject_layers: tuple = (12,)    # legacy absolute; resolved from inject_layer_fracs
    inject_layer_fracs: tuple = (0.43,)  # fraction(s) of n_layers (~12/28)

    # Steering strength. With alpha_relative=True the unit primer is scaled to a
    # FRACTION of the local residual-stream norm (alpha_eff = alpha * ||h||), so
    # the same alpha is a comparable nudge across model sizes. Absolute alpha is
    # not transferable: the residual norm grows with hidden size/depth, so a
    # fixed alpha that steers a 1.5B is far too weak in a 32B.
    alpha_relative: bool = True
    alpha: float = 0.10             # fraction of residual norm (sweep 0.04..0.3)

    # Where we read activations when EXTRACTING a primer (resolved from frac).
    extract_layer: int = 12         # legacy absolute fallback
    extract_layer_frac: float = 0.43

    # Primer extraction regime (INVARIANT #4: extract in the regime you inject in).
    #   "compressed" -> contrast (contract+summary) vs (summary): isolates the
    #                   working-mode direction ON TOP of the compressed-prompt
    #                   distribution where the primer is actually injected.
    #   "contract"   -> legacy contrast (contract+instruction) vs (instruction),
    #                   built from full-style activations (distribution mismatch).
    extract_regime: str = "compressed"

    # Compression
    compress_ratio: float = 0.25    # target summary length as fraction of original

    # Which domains + which split to evaluate (train builds the primer, val tunes
    # alpha/layer in sweep.py, test is the held-out report).
    domains: tuple = ("coding", "math", "writing")
    eval_split: str = "test"

    # Multi-seed variance (INVARIANT #8). The reported number is greedy and
    # deterministic; for a variance study set eval_temperature>0 and several
    # seeds, then report mean +/- std. With temperature=0, seeds collapse to one
    # run (greedy is seed-invariant), so the default stays reproducible.
    seeds: tuple = (0,)
    eval_temperature: float = 0.0

    # Sweep grid (sweep.py selects on the VAL split, reports on TEST). Layers are
    # swept as FRACTIONS of depth so the grid covers mid-stack at every size:
    # (0.3,0.43,0.57,0.7) maps to ~(8,12,16,20) on a 28-layer model and to
    # ~(19,28,36,45) on a 64-layer 32B. Alphas are fractions of residual norm.
    sweep_alphas: tuple = (0.04, 0.08, 0.12, 0.20, 0.30)
    sweep_layer_fracs: tuple = (0.3, 0.43, 0.57, 0.7)
    sweep_layers: tuple = (8, 12, 16, 20)   # legacy absolute fallback
    content_tolerance: float = 0.1          # max allowed content drop when picking

    # Capability gate (INVARIANT #3 applied to the conformance head). Only count a
    # (model, domain) cell as evidence about priming if the `full` arm clears this
    # conformance bar; below it the headroom is capability-bound, not regime-bound.
    capability_gate: float = 0.8

    # Scale ladder (scale_ladder.py): identical harness across model sizes to test
    # whether the primer effect / rival gap grows with parameters. 7B+ needs 4bit.
    #
    # 14B/32B need an A100 (32B-4bit ~18-20GB will not fit a 16GB T4). The ladder
    # sweeps EACH model on its own val split (depth/norm-relative grid) before
    # the test report, so no model inherits another's operating point.
    model_ladder: tuple = (
        dict(model_name="Qwen/Qwen2.5-1.5B-Instruct", load_in_4bit=False),
        dict(model_name="Qwen/Qwen2.5-3B-Instruct", load_in_4bit=False),
        dict(model_name="Qwen/Qwen2.5-7B-Instruct", load_in_4bit=True),
        dict(model_name="Qwen/Qwen2.5-14B-Instruct", load_in_4bit=True),
        dict(model_name="Qwen/Qwen2.5-32B-Instruct", load_in_4bit=True),
    )

    # Generation
    max_new_tokens: int = 512
    temperature: float = 0.0        # greedy for reproducible pass@1
    seed: int = 0

    bank_path: str = "primer_bank"  # folder for saved primers
    results_path: str = "results.json"
