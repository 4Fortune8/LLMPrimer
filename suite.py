"""Multi-domain task suite with train / validation / test splits.

Each DOMAIN supplies, for the priming experiment:
  - contract       : the working-mode / house-style text the primer steers toward
                     (and that neutral compression is expected to erode)
  - prior_session  : styled, solved examples = the `full` arm context
  - tasks          : list of task dicts, each tagged split in {train, val, test}

How the splits map onto a steering-vector experiment:
  - train  -> contrastive pairs that BUILD the primer (extraction set)
  - val    -> held-out tasks used to SELECT alpha x layer (the sweep; see sweep.py)
  - test   -> held-out tasks for the FINAL reported number (+ rival baselines)

INVARIANTS honored (see AGENTS.md):
  * Heads orthogonal: the content scorer checks valid-output FACTS only; the
    contract (style / format / register) is scored ONLY by the conformance head.
  * No leak: the primer is extracted from TRAIN tasks; val/test never feed it.
  * Solvable: tasks are deliberately easy so the `full` arm keeps content ~1.0 —
    headroom must live in conformance, not raw capability.
"""

# ===========================================================================
# CODING
# ===========================================================================
CODING_CONTRACT = (
    "House style for all functions:\n"
    "- snake_case names\n"
    "- full type hints on every parameter and the return value\n"
    "- raise ValueError with a clear message on invalid input\n"
    "- a one-line Google-style docstring\n"
)

CODING_SESSION = CODING_CONTRACT + """
Example solved tasks (house style):

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

CODING_TASKS = [
    # --- train (build the primer) -----------------------------------------
    dict(split="train", id="reverse_string",
         instruction="Write a function `reverse_string(text: str) -> str` that "
                     "returns the string reversed.",
         content=dict(kind="unittest", tests="""
assert reverse_string("abc") == "cba"
assert reverse_string("") == ""
""")),
    dict(split="train", id="is_palindrome",
         instruction="Write a function `is_palindrome(text: str) -> bool` that "
                     "reports whether text reads the same backwards.",
         content=dict(kind="unittest", tests="""
assert is_palindrome("aba") is True
assert is_palindrome("ab") is False
""")),
    dict(split="train", id="sum_list",
         instruction="Write a function `sum_list(nums: list) -> int` returning "
                     "the sum of the numbers.",
         content=dict(kind="unittest", tests="""
assert sum_list([1,2,3]) == 6
assert sum_list([]) == 0
""")),
    dict(split="train", id="count_words",
         instruction="Write a function `count_words(text: str) -> int` returning "
                     "the number of whitespace-separated words.",
         content=dict(kind="unittest", tests="""
assert count_words("a b c") == 3
assert count_words("") == 0
""")),
    # --- val (select alpha x layer) ---------------------------------------
    dict(split="val", id="factorial",
         instruction="Write a function `factorial(n: int) -> int` returning n!.",
         content=dict(kind="unittest", tests="""
assert factorial(0) == 1
assert factorial(5) == 120
""")),
    dict(split="val", id="max_in_list",
         instruction="Write a function `max_in_list(nums: list) -> int` returning "
                     "the largest number.",
         content=dict(kind="unittest", tests="""
assert max_in_list([1,5,3]) == 5
assert max_in_list([-2,-9]) == -2
""")),
    dict(split="val", id="celsius_to_fahrenheit",
         instruction="Write a function `celsius_to_fahrenheit(c: float) -> float` "
                     "converting Celsius to Fahrenheit.",
         content=dict(kind="unittest", tests="""
assert celsius_to_fahrenheit(0) == 32
assert celsius_to_fahrenheit(100) == 212
""")),
    dict(split="val", id="count_evens",
         instruction="Write a function `count_evens(nums: list) -> int` returning "
                     "how many numbers are even.",
         content=dict(kind="unittest", tests="""
assert count_evens([1,2,3,4]) == 2
assert count_evens([]) == 0
""")),
    dict(split="val", id="capitalize_words",
         instruction="Write a function `capitalize_words(text: str) -> str` that "
                     "upper-cases the first letter of each word.",
         content=dict(kind="unittest", tests="""
assert capitalize_words("hello world") == "Hello World"
assert capitalize_words("") == ""
""")),
    # --- test (final report) ----------------------------------------------
    dict(split="test", id="dedupe_preserve_order",
         instruction="Write a function `dedupe(items: list) -> list` that removes "
                     "duplicates while preserving first-seen order.",
         content=dict(kind="unittest", tests="""
assert dedupe([1,1,2,3,2]) == [1,2,3]
assert dedupe([]) == []
assert dedupe(['a','b','a']) == ['a','b']
""")),
    dict(split="test", id="word_frequencies",
         instruction="Write a function `word_freq(text: str) -> dict` mapping each "
                     "lowercased word to its count.",
         content=dict(kind="unittest", tests="""
assert word_freq("a a b") == {"a":2,"b":1}
assert word_freq("") == {}
""")),
    dict(split="test", id="running_max",
         instruction="Write a function `running_max(nums: list) -> list` returning "
                     "the cumulative maximum at each index.",
         content=dict(kind="unittest", tests="""
assert running_max([1,3,2,5]) == [1,3,3,5]
assert running_max([]) == []
""")),
    dict(split="test", id="average",
         instruction="Write a function `average(nums: list) -> float` returning "
                     "the arithmetic mean of the numbers.",
         content=dict(kind="unittest", tests="""
assert average([2,4]) == 3
assert average([5]) == 5
""")),
    dict(split="test", id="flatten",
         instruction="Write a function `flatten(matrix: list) -> list` that "
                     "concatenates a list of lists into one flat list.",
         content=dict(kind="unittest", tests="""
assert flatten([[1,2],[3]]) == [1,2,3]
assert flatten([[],[1]]) == [1]
""")),
]

# ===========================================================================
# MATH / PROBLEM SOLVING  (GSM8K-style, kept easy so the model can solve them)
# ===========================================================================
MATH_CONTRACT = (
    "Working mode for every problem:\n"
    "- reason in numbered steps, each line starting 'Step N:'\n"
    "- show the explicit arithmetic on each step\n"
    "- finish with a final line exactly: 'Answer: <number>'\n"
)

MATH_SESSION = MATH_CONTRACT + """
Example solved problem (working mode):

Problem: A crate holds 3 rows of 4 jars. How many jars?
Step 1: multiply rows by jars per row = 3 * 4 = 12
Answer: 12

Problem: Mia had 10 stickers, gave away 3, then earned 5. How many now?
Step 1: subtract given away = 10 - 3 = 7
Step 2: add earned = 7 + 5 = 12
Answer: 12
"""

MATH_TASKS = [
    # --- train ------------------------------------------------------------
    dict(split="train", id="apples_box",
         instruction="A box has 6 bags with 4 apples each. How many apples in total?",
         content=dict(kind="numeric", answer=24)),
    dict(split="train", id="coins_spend",
         instruction="Leo has 15 coins, spends 6, then finds 4. How many coins now?",
         content=dict(kind="numeric", answer=13)),
    dict(split="train", id="muffin_trays",
         instruction="A baker makes 5 trays of 8 muffins. How many muffins in total?",
         content=dict(kind="numeric", answer=40)),
    dict(split="train", id="marbles",
         instruction="Tom has 9 marbles, buys 7 more, then loses 2. How many now?",
         content=dict(kind="numeric", answer=14)),
    # --- val --------------------------------------------------------------
    dict(split="val", id="trip_distance",
         instruction="A car drives 60 km in the morning and 90 km in the afternoon. "
                     "How many km in total?",
         content=dict(kind="numeric", answer=150)),
    dict(split="val", id="share_candy",
         instruction="There are 24 candies shared equally among 6 children. "
                     "How many candies does each child get?",
         content=dict(kind="numeric", answer=4)),
    dict(split="val", id="discount_price",
         instruction="A shirt costs 20 dollars and has a 10 percent discount. "
                     "What is the final price in dollars?",
         content=dict(kind="numeric", answer=18)),
    dict(split="val", id="classroom",
         instruction="A class has 4 rows of 7 students. How many students in total?",
         content=dict(kind="numeric", answer=28)),
    dict(split="val", id="wallet_left",
         instruction="Sara had 30 dollars, spent 12 on lunch and 8 on a book. "
                     "How much money is left?",
         content=dict(kind="numeric", answer=10)),
    # --- test -------------------------------------------------------------
    dict(split="test", id="pages_left",
         instruction="A book has 120 pages. Ada read 45 pages on Monday and 35 on "
                     "Tuesday. How many pages are left?",
         content=dict(kind="numeric", answer=40)),
    dict(split="test", id="hen_eggs",
         instruction="A farmer has 5 hens and each lays 6 eggs. How many eggs in total?",
         content=dict(kind="numeric", answer=30)),
    dict(split="test", id="tank_left",
         instruction="A tank holds 50 liters. 18 liters are used in the morning and "
                     "12 in the evening. How many liters are left?",
         content=dict(kind="numeric", answer=20)),
    dict(split="test", id="split_bill",
         instruction="Three friends split a 60 dollar bill equally. How much does "
                     "each person pay in dollars?",
         content=dict(kind="numeric", answer=20)),
    dict(split="test", id="weekly_run",
         instruction="A runner runs 8 km each day for 5 days. How many km in total?",
         content=dict(kind="numeric", answer=40)),
]

# ===========================================================================
# WRITING  (short explanations; content = fact coverage, conformance = register)
# ===========================================================================
WRITING_CONTRACT = (
    "House register for every explanation:\n"
    "- address the reader directly in the second person ('you')\n"
    "- no contractions (write 'do not', not \"don't\")\n"
    "- present the key points as a bulleted list using '-'\n"
)

WRITING_SESSION = WRITING_CONTRACT + """
Example explanation (house register):

Explain what evaporation is.
- You can think of evaporation as the way a liquid changes into a gas.
- It happens when molecules gain enough energy to leave the surface.
- You will notice it speeds up as the temperature rises.
"""

WRITING_TASKS = [
    # --- train ------------------------------------------------------------
    dict(split="train", id="photosynthesis",
         instruction="Explain what photosynthesis is.",
         content=dict(kind="coverage", keywords=[["light", "sunlight"],
                      ["carbon dioxide", "co2"], ["oxygen"], ["glucose", "sugar"]])),
    dict(split="train", id="cpu",
         instruction="Explain what a computer's CPU does.",
         content=dict(kind="coverage", keywords=[["instruction"],
                      ["process", "execute", "calculat"], ["program", "computer"]])),
    dict(split="train", id="water_cycle",
         instruction="Explain the water cycle.",
         content=dict(kind="coverage", keywords=[["evaporat"],
                      ["condens"], ["precipitat", "rain"]])),
    dict(split="train", id="digestion",
         instruction="Explain what digestion is.",
         content=dict(kind="coverage", keywords=[["food"],
                      ["stomach", "intestine"], ["nutrient", "energy", "absorb"]])),
    # --- val --------------------------------------------------------------
    dict(split="val", id="rain",
         instruction="Explain what rain is.",
         content=dict(kind="coverage", keywords=[["water"], ["cloud"],
                      ["condens", "evaporat", "vapour", "vapor"]])),
    dict(split="val", id="recycling",
         instruction="Explain what recycling is.",
         content=dict(kind="coverage", keywords=[["waste", "material"],
                      ["reuse", "process"], ["environment", "resource"]])),
    dict(split="val", id="magnet",
         instruction="Explain what a magnet does.",
         content=dict(kind="coverage", keywords=[["force", "field"],
                      ["attract", "repel"], ["metal", "iron", "pole"]])),
    dict(split="val", id="battery",
         instruction="Explain what a battery does.",
         content=dict(kind="coverage", keywords=[["energy", "electric"],
                      ["store", "chemical"], ["power", "device"]])),
    dict(split="val", id="echo",
         instruction="Explain what an echo is.",
         content=dict(kind="coverage", keywords=[["sound"],
                      ["reflect", "bounce"], ["surface", "wall"]])),
    # --- test -------------------------------------------------------------
    dict(split="test", id="gravity",
         instruction="Explain what gravity is.",
         content=dict(kind="coverage", keywords=[["force"], ["mass", "object"],
                      ["attract", "pull"]])),
    dict(split="test", id="vaccine",
         instruction="Explain what a vaccine does.",
         content=dict(kind="coverage", keywords=[["immune", "immunity"],
                      ["disease", "infection", "virus"], ["protect", "prevent"]])),
    dict(split="test", id="tides",
         instruction="Explain what causes ocean tides.",
         content=dict(kind="coverage", keywords=[["moon"], ["gravit"],
                      ["water", "ocean", "sea"]])),
    dict(split="test", id="friction",
         instruction="Explain what friction is.",
         content=dict(kind="coverage", keywords=[["force"],
                      ["surface", "contact"], ["motion", "move", "slow"]])),
    dict(split="test", id="evaporation",
         instruction="Explain what evaporation is.",
         content=dict(kind="coverage", keywords=[["liquid"],
                      ["gas", "vapour", "vapor"], ["heat", "energy", "temperature"]])),
]

# ===========================================================================
# Registry
# ===========================================================================
DOMAINS = {
    "coding": dict(contract=CODING_CONTRACT, session=CODING_SESSION,
                   tasks=CODING_TASKS,
                   descriptor="coding python house style type hints docstring valueerror snake_case"),
    "math": dict(contract=MATH_CONTRACT, session=MATH_SESSION,
                 tasks=MATH_TASKS,
                 descriptor="math problem solving step by step numbered answer arithmetic"),
    "writing": dict(contract=WRITING_CONTRACT, session=WRITING_SESSION,
                    tasks=WRITING_TASKS,
                    descriptor="writing explanation second person no contractions bullets register"),
}


def tasks_for(domain, split):
    """Return the tasks in `domain` belonging to `split` ('train'|'val'|'test')."""
    return [t for t in DOMAINS[domain]["tasks"] if t["split"] == split]


def extraction_pairs(domain):
    """Contrastive (mode_on, mode_off) pairs built from the TRAIN split only.

    mode_on carries the contract (the working mode); mode_off is the bare task.
    The mean difference isolates the regime direction (the primer)."""
    contract = DOMAINS[domain]["contract"]
    pairs = []
    for t in tasks_for(domain, "train"):
        pairs.append((contract + "\n" + t["instruction"], t["instruction"]))
    return pairs
