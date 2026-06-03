"""A small coding task-family with an explicit 'house style' (the working mode).

Design goal: pick tasks the base model can already SOLVE (so the content head has
headroom to stay high), and make the differentiator the STYLE conformance — that
is where the difficulty hierarchy in the function-vector literature predicts
primers actually help. If you instead use tasks the model can't solve, expect
~zero recovery on the content head and learn little.

Each task: an instruction, a function name, and assert-based hidden tests.
The HOUSE STYLE is the regime we extract a primer for and that compression erodes.
"""

HOUSE_STYLE = (
    "House style for all functions:\n"
    "- snake_case names\n"
    "- full type hints on every parameter and the return value\n"
    "- raise ValueError with a clear message on invalid input\n"
    "- a one-line Google-style docstring\n"
)

# ---- prior 'session': solved tasks rendered in-house-style -----------------
PRIOR_SESSION = HOUSE_STYLE + """
Example solved task (house style):

def count_vowels(text: str) -> int:
    \"\"\"Return the number of vowels in text.\"\"\"
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    return sum(1 for c in text.lower() if c in "aeiou")

def clamp(value: float, low: float, high: float) -> float:
    \"\"\"Clamp value to the inclusive range [low, high].\"\"\"
    if low > high:
        raise ValueError("low must not exceed high")
    return max(low, min(high, value))
"""

# ---- current tasks to solve ------------------------------------------------
TASKS = [
    dict(
        id="dedupe_preserve_order",
        descriptor="list deduplicate preserve order house style python",
        instruction="Write a function `dedupe(items: list) -> list` that removes "
                    "duplicates while preserving first-seen order.",
        # content head = valid-input behaviour ONLY. Error-handling/contract is
        # measured by the conformance head (raises_valueerror), so the two heads
        # stay orthogonal. Do not re-add contract asserts here.
        tests="""
assert dedupe([1,1,2,3,2]) == [1,2,3]
assert dedupe([]) == []
assert dedupe(['a','b','a']) == ['a','b']
""",
    ),
    dict(
        id="word_frequencies",
        descriptor="string word frequency count dict house style python",
        instruction="Write a function `word_freq(text: str) -> dict` mapping each "
                    "lowercased word to its count.",
        tests="""
assert word_freq("a a b") == {"a":2,"b":1}
assert word_freq("") == {}
""",
    ),
    dict(
        id="running_max",
        descriptor="list running maximum cumulative house style python",
        instruction="Write a function `running_max(nums: list) -> list` returning "
                    "the cumulative maximum at each index.",
        tests="""
assert running_max([1,3,2,5]) == [1,3,3,5]
assert running_max([]) == []
""",
    ),
]


def extraction_pairs():
    """Contrastive (mode_on, mode_off) pairs for primer extraction. mode_on
    carries the house style + a styled example; mode_off is the bare task."""
    pairs = []
    for t in TASKS:
        on = HOUSE_STYLE + "\n" + t["instruction"]
        off = t["instruction"]
        pairs.append((on, off))
    return pairs
