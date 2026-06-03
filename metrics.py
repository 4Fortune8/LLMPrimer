"""Two SEPARATE metric heads.

content_score   -> did the facts survive? (functional correctness, pass@1)
conformance_score -> did the working mode survive? (house-style adherence via AST)

Keeping them separate is the whole point: the hypothesis predicts re-injected
primers barely move content but visibly move conformance over the compressed
baseline, at near-zero added cost.
"""
import ast
import re
import subprocess
import sys
import tempfile
import textwrap


def extract_code(text):
    """Pull the first python code block, else assume the whole thing is code."""
    m = re.search(r"```(?:python)?\s*(.*?)```", text, re.DOTALL)
    return (m.group(1) if m else text).strip()


# ---- CONTENT HEAD ----------------------------------------------------------
def content_score(generation, tests, timeout=10):
    code = extract_code(generation)
    program = code + "\n\n" + textwrap.dedent(tests)
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(program)
        path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True,
                           timeout=timeout, text=True)
        return 1.0 if r.returncode == 0 else 0.0
    except subprocess.TimeoutExpired:
        return 0.0


# ---- CONFORMANCE HEAD ------------------------------------------------------
def conformance_score(generation):
    """Fraction of house-style checks passed. Returns (score, breakdown)."""
    code = extract_code(generation)
    checks = {"snake_case": False, "type_hints": False,
              "raises_valueerror": False, "docstring": False}
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 0.0, checks  # didn't even parse -> zero conformance

    funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    if not funcs:
        return 0.0, checks
    fn = funcs[0]

    checks["snake_case"] = bool(re.fullmatch(r"[a-z_][a-z0-9_]*", fn.name))
    args_ok = all(a.annotation is not None for a in fn.args.args)
    checks["type_hints"] = args_ok and fn.returns is not None
    checks["docstring"] = ast.get_docstring(fn) is not None
    checks["raises_valueerror"] = any(
        isinstance(n, ast.Raise) and "ValueError" in ast.dump(n)
        for n in ast.walk(fn)
    )
    score = sum(checks.values()) / len(checks)
    return score, checks
