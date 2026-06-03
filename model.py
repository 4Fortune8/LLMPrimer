"""Model wrapper with residual-stream hooks for capturing and injecting primers.

Works with standard HF decoder LMs (Llama/Qwen/Mistral families) where the
decoder layers live at `model.model.layers` and each layer returns a tuple whose
first element is the residual-stream hidden state [batch, seq, hidden].
"""
from contextlib import contextmanager
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class HookedLM:
    def __init__(self, cfg):
        self.cfg = cfg
        dtype = getattr(torch, cfg.dtype)
        kwargs = dict(torch_dtype=dtype, device_map=cfg.device)
        if cfg.load_in_4bit:
            from transformers import BitsAndBytesConfig
            kwargs.pop("torch_dtype")
            kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True, bnb_4bit_compute_dtype=dtype
            )
        self.tok = AutoTokenizer.from_pretrained(cfg.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(cfg.model_name, **kwargs)
        self.model.eval()
        self.layers = self.model.model.layers
        self.hidden = self.model.config.hidden_size

    # ---- prompt formatting -------------------------------------------------
    def render(self, system, user):
        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.append({"role": "user", "content": user})
        ids = self.tok.apply_chat_template(
            msgs, add_generation_prompt=True, return_tensors="pt",
            return_dict=False,
        )
        # Newer transformers may still return a BatchEncoding/dict; the rest of
        # the harness expects a plain [batch, seq] tensor.
        if not isinstance(ids, torch.Tensor):
            ids = ids["input_ids"]
        return ids.to(self.model.device)

    # ---- capturing a residual at a layer (for extraction) ------------------
    @torch.no_grad()
    def last_token_residual(self, input_ids, layer):
        """Return the residual-stream vector at `layer` for the final token."""
        store = {}

        def cap(mod, inp, out):
            store["h"] = (out[0] if isinstance(out, tuple) else out).detach()

        h = self.layers[layer].register_forward_hook(cap)
        try:
            self.model(input_ids)
        finally:
            h.remove()
        return store["h"][0, -1, :].float().cpu()  # [hidden]

    # ---- injecting primers during a forward/generate -----------------------
    @contextmanager
    def inject(self, primers):
        """primers: list of (layer:int, vector:Tensor[hidden], alpha:float).
        Adds alpha*vector to the residual stream at the given layer for every
        position in every forward pass within the context."""
        handles = []
        dev = self.model.device
        by_layer = {}
        for layer, vec, alpha in primers:
            v = (alpha * vec.to(dev).to(self.model.dtype))
            by_layer.setdefault(layer, torch.zeros(self.hidden, device=dev,
                                                    dtype=self.model.dtype))
            by_layer[layer] = by_layer[layer] + v

        def make(delta):
            def hook(mod, inp, out):
                if isinstance(out, tuple):
                    return (out[0] + delta,) + tuple(out[1:])
                return out + delta
            return hook

        try:
            for layer, delta in by_layer.items():
                handles.append(self.layers[layer].register_forward_hook(make(delta)))
            yield
        finally:
            for h in handles:
                h.remove()

    # ---- generation --------------------------------------------------------
    @torch.no_grad()
    def generate(self, input_ids, primers=None):
        cfg = self.cfg
        torch.manual_seed(cfg.seed)
        gen_kwargs = dict(
            max_new_tokens=cfg.max_new_tokens,
            do_sample=cfg.temperature > 0,
            pad_token_id=self.tok.eos_token_id,
        )
        if cfg.temperature > 0:
            gen_kwargs["temperature"] = cfg.temperature
        ctx = self.inject(primers) if primers else _null()
        with ctx:
            out = self.model.generate(input_ids, **gen_kwargs)
        text = self.tok.decode(out[0, input_ids.shape[1]:], skip_special_tokens=True)
        return text


@contextmanager
def _null():
    yield
