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


# ===========================================================================
# MATH domain
# ===========================================================================
def _last_number(text):
    """Return the last number that follows an 'Answer:' label if present, else
    the last number anywhere. Returns float or None."""
    m = re.findall(r"[Aa]nswer\s*:?\s*\$?(-?\d+(?:\.\d+)?)", text)
    if not m:
        m = re.findall(r"-?\d+(?:\.\d+)?", text)
    if not m:
        return None
    try:
        return float(m[-1])
    except ValueError:
        return None


def math_content_score(generation, answer):
    """1.0 if the model's final number equals the gold answer (facts survived)."""
    got = _last_number(generation)
    if got is None:
        return 0.0
    return 1.0 if abs(got - float(answer)) < 1e-6 else 0.0


def math_conformance_score(generation):
    """Working-mode contract: numbered steps, shown arithmetic, 'Answer:' line."""
    g = generation
    checks = {
        "numbered_steps": len(re.findall(r"(?im)^\s*step\s*\d+\s*:", g)) >= 2,
        "shows_arithmetic": bool(re.search(r"\d\s*[\+\-\*/x]\s*\d", g)),
        "answer_line": bool(re.search(r"(?im)^\s*answer\s*:\s*-?\d", g)),
        "no_prose_intro": g.strip().lower().startswith("step"),
    }
    return sum(checks.values()) / len(checks), checks


# ===========================================================================
# WRITING domain
# ===========================================================================
_CONTRACTION = re.compile(r"\b\w+'(t|re|s|ll|ve|d|m)\b", re.I)


def writing_content_score(generation, keywords):
    """Fraction of required fact-groups covered. Each group is a list of
    acceptable substrings (any one counts). Facts only; register is separate."""
    if not keywords:
        return 0.0
    g = generation.lower()
    hit = sum(any(alt.lower() in g for alt in group) for group in keywords)
    return hit / len(keywords)


def writing_conformance_score(generation):
    """House register: second person, no contractions, bulleted list."""
    g = generation
    bullets = len(re.findall(r"(?m)^\s*[-*\u2022]\s+\S", g))
    checks = {
        "second_person": bool(re.search(r"\byou\b|\byour\b", g, re.I)),
        "no_contractions": _CONTRACTION.search(g) is None,
        "bulleted_list": bullets >= 2,
    }
    return sum(checks.values()) / len(checks), checks


# ===========================================================================
# Domain dispatch
# ===========================================================================
def score_content(domain, generation, content_spec):
    """Domain-aware content head (did the facts survive?)."""
    kind = content_spec["kind"]
    if kind == "unittest":
        return content_score(generation, content_spec["tests"])
    if kind == "numeric":
        return math_content_score(generation, content_spec["answer"])
    if kind == "coverage":
        return writing_content_score(generation, content_spec["keywords"])
    raise ValueError(f"unknown content kind: {kind}")


def score_conformance(domain, generation):
    """Domain-aware conformance head (did the working mode survive?)."""
    if domain == "coding":
        return conformance_score(generation)
    if domain == "math":
        return math_conformance_score(generation)
    if domain == "writing":
        return writing_conformance_score(generation)
    raise ValueError(f"unknown domain: {domain}")
