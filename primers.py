"""Extract, store, and retrieve 'primers' (working-mode steering vectors).

Extraction follows the function-vector / ActAdd recipe: take the mean DIFFERENCE
between the final-token residual on a 'mode-on' prompt (carrying the working mode
/ house style / demonstrations) and a matched 'mode-off' prompt (bare task). The
difference, averaged over many pairs, isolates the regime direction and strips
the problem-specific content — which is exactly the slice we expect to survive
compression poorly and to be cheap to re-inject.
"""
import json
import os
import torch


def extract_primer(lm, pairs, layer):
    """pairs: list of (mode_on_text, mode_off_text), each a fully-rendered user
    string. Returns a unit-norm direction [hidden] (apply scale via alpha)."""
    diffs = []
    for on_text, off_text in pairs:
        on = lm.last_token_residual(lm.render(None, on_text), layer)
        off = lm.last_token_residual(lm.render(None, off_text), layer)
        diffs.append(on - off)
    d = torch.stack(diffs).mean(0)
    return d / (d.norm() + 1e-8)


class PrimerBank:
    """Tiny on-disk catalogue. Each primer: a small vector (~hidden*2 bytes) plus
    a text descriptor used for retrieval. Storage is trivially cheap."""

    def __init__(self, path):
        self.path = path
        os.makedirs(path, exist_ok=True)

    def save(self, pid, vector, layer, descriptor, alpha):
        torch.save(vector, os.path.join(self.path, f"{pid}.pt"))
        meta = dict(pid=pid, layer=layer, descriptor=descriptor, alpha=alpha)
        with open(os.path.join(self.path, f"{pid}.json"), "w") as f:
            json.dump(meta, f, indent=2)

    def _all_meta(self):
        out = []
        for fn in os.listdir(self.path):
            if fn.endswith(".json"):
                with open(os.path.join(self.path, fn)) as f:
                    out.append(json.load(f))
        return out

    def load(self, pid):
        with open(os.path.join(self.path, f"{pid}.json")) as f:
            meta = json.load(f)
        vec = torch.load(os.path.join(self.path, f"{pid}.pt"))
        return vec, meta

    def retrieve(self, query, k=1):
        """Baseline retrieval: Jaccard overlap on descriptor keywords. This is the
        deliberately-simple selector — replace with embedding cosine (e.g.
        sentence-transformers) once you want to study the selection layer itself,
        which is the genuinely open research question."""
        q = set(query.lower().split())
        scored = []
        for m in self._all_meta():
            d = set(m["descriptor"].lower().split())
            j = len(q & d) / (len(q | d) + 1e-8)
            scored.append((j, m["pid"]))
        scored.sort(reverse=True)
        return [pid for _, pid in scored[:k]]

    def as_injection(self, pids, alpha_override=None):
        prim = []
        for pid in pids:
            vec, meta = self.load(pid)
            prim.append((meta["layer"], vec,
                         alpha_override if alpha_override is not None else meta["alpha"]))
        return prim
