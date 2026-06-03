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
    inject_layers: tuple = (12,)    # e.g. (10, 14) for two primers
    alpha: float = 6.0              # steering strength; sweep this (2..12)

    # Where we read activations when EXTRACTING a primer.
    extract_layer: int = 12

    # Compression
    compress_ratio: float = 0.25    # target summary length as fraction of original

    # Which domains + which split to evaluate (train builds the primer, val tunes
    # alpha/layer in sweep.py, test is the held-out report).
    domains: tuple = ("coding", "math", "writing")
    eval_split: str = "test"

    # Sweep grid (sweep.py selects on the VAL split, reports on TEST).
    sweep_alphas: tuple = (2.0, 4.0, 6.0, 8.0, 10.0, 12.0)
    sweep_layers: tuple = (8, 12, 16, 20)   # mid-stack for a ~28-layer 1.5B
    content_tolerance: float = 0.1          # max allowed content drop when picking

    # Generation
    max_new_tokens: int = 512
    temperature: float = 0.0        # greedy for reproducible pass@1
    seed: int = 0

    bank_path: str = "primer_bank"  # folder for saved primers
    results_path: str = "results.json"
