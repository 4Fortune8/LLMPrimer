# Primer harness run (Qwen/Qwen2.5-3B-Instruct, split=test, seeds=[0], regime=compressed)

## Overall

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| zero_shot | 1.00 | 0.24 +/-0.22 | 53 |
| full | 1.00 | 0.89 +/-0.14 | 203 |
| compressed | 0.93 | 0.56 +/-0.36 | 92 |
| style_text | 0.84 | 0.72 +/-0.27 | 136 |
| primed | 0.93 | 0.60 +/-0.33 | 92 |

## Value (cost-adjusted: primer vs re-pasted text rival)

| scope | conf gain vs compressed | conf vs style_text | tokens vs style_text | verdict |
|---|---|---|---|---|
| coding | +0.05 | +0.25 | -43 | primer dominates rival |
| math | +0.00 | -0.35 | -43 | mixed (trade-off) |
| writing | +0.07 | -0.27 | -46 | mixed (trade-off) |
| **gated overall** | +0.04 | -0.12 | -44 | mixed (trade-off) |

## Domain: coding (full conformance=0.95 -> PASS)

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| zero_shot | 1.00 | 0.50 +/-0.00 | 61 |
| full | 1.00 | 0.95 +/-0.11 | 235 |
| compressed | 0.80 | 0.95 +/-0.11 | 112 |
| style_text | 0.60 | 0.75 +/-0.43 | 155 |
| primed | 0.80 | 1.00 +/-0.00 | 112 |

### dedupe_preserve_order

> Write a function `dedupe(items: list) -> list` that removes duplicates while preserving first-seen order.

**zero_shot** — content=1.00 conformance=0.50 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=x)

```
```python
def dedupe(items: list) -> list:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```
```

**full** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
def dedupe(items: list) -> list:
    """
    Remove duplicates from items while preserving the first-seen order.
    """
    seen = set()
    unique_items = []
    for item in items:
        if item not in seen:
            unique_items.append(item)
            seen.add(item)
    return unique_items
```
```

**compressed** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
def dedupe(items: list) -> list:
    """
    Removes duplicate values from a list while preserving the order of items.

    Args:
    items (list): The input list containing elements which may or may not be unique.

    Returns:
    list: A new list with duplicates removed and original order preserved.
    """
    seen = set()
    unique_items = []
    for item in items:
        if item not in seen:
            unique_items.append(item)
            seen.add(item)
    return unique_items
```
```

**style_text** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
def dedupe(items: list) -> list:
    """
    Removes duplicates from a list while preserving the order of items.
    
    Args:
    items (list): The list from which to remove duplicates.
    
    Returns:
    list: A new list with duplicates removed.
    
    Raises:
    ValueError: If the input is not a list.
    """
    seen = set()
    unique_items = []
    for item in items:
        if item not in seen:
            unique_items.append(item)
            seen.add(item)
    return unique_items
```
```

**primed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def dedupe(items: list) -> list:
    """
    Removes duplicate values from a list while preserving the order of items.
    
    Args:
    items (list): The list from which to remove duplicates.
    
    Returns:
    list: A new list with duplicates removed and original order preserved.
    
    Raises:
    ValueError: If the input is not a list.
    """
    if not isinstance(items, list):
        raise ValueError("Input must be a list.")
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```
```

### word_frequencies

> Write a function `word_freq(text: str) -> dict` mapping each lowercased word to its count.

**zero_shot** — content=1.00 conformance=0.50 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=x)

```
```python
def word_freq(text: str) -> dict:
    # Convert text to lowercase and split into words
    words = text.lower().split()
    
    # Initialize an empty dictionary to store word counts
    freq_dict = {}
    
    # Iterate over each word in the list
    for word in words:
        # If the word is already in the dictionary, increment its count
        if word in freq_dict:
            freq_dict[word] += 1
        # Otherwise, add the word to the dictionary with a count of 1
        else:
            freq_dict[word] = 1
    
    return freq_dict
```
```

**full** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def word_freq(text: str) -> dict:
    """Map each lowercased word in text to its count."""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    
    word_count = {}
    words = text.lower().split()
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    
    return word_count
```
```

**compressed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def word_freq(text: str) -> dict:
    """
    Maps each unique word (in lowercase) to its frequency in the given text.
    
    Args:
    text (str): The input text from which to compute word frequencies.
    
    Returns:
    dict: A dictionary where keys are words (in lowercase) and values are their respective counts.
    
    Raises:
    ValueError: If the input is not a string.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    # Convert text to lowercase and split into words
    words = text.lower().split()
    
    # Count occurrences of each word
    freq = {}
    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    
    return freq
```
```

**style_text** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def word_freq(text: str) -> dict:
    """
    Maps each lowercased word in the input text to its count.
    
    Args:
    text (str): The input string to analyze.

    Returns:
    dict: A dictionary where keys are lowercased words and values are their counts.
    
    Raises:
    ValueError: If the input is not a string.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    word_count = {}
    for word in text.lower().split():
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count
```
```

**primed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def word_freq(text: str) -> dict:
    """
    Maps each lowercased word in the input text to its frequency.
    
    Args:
    text (str): The input string to analyze.
    
    Returns:
    dict: A dictionary where keys are words (in lowercase) and values are their frequencies.
    
    Raises:
    ValueError: If the input is not a string.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    word_list = text.lower().split()
    freq_map = {}
    for word in word_list:
        if word in freq_map:
            freq_map[word] += 1
        else:
            freq_map[word] = 1
    
    return freq_map
```
```

### running_max

> Write a function `running_max(nums: list) -> list` returning the cumulative maximum at each index.

**zero_shot** — content=1.00 conformance=0.50 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=x)

```
```python
def running_max(nums: list) -> list:
    if not nums:
        return []
    
    result = [nums[0]]
    for num in nums[1:]:
        result.append(max(num, result[-1]))
    return result
```
```

**full** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def running_max(nums: list) -> list:
    """Return a list where each element is the running maximum up to that index in nums."""
    if not all(isinstance(x, (int, float)) for x in nums):
        raise ValueError("All elements in nums must be numbers")
    result = []
    current_max = float('-inf')
    for num in nums:
        current_max = max(current_max, num)
        result.append(current_max)
    return result
```
```

**compressed** — content=0.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def running_max(nums: list) -> list:
    """
    Returns a list where each element is the running maximum up to that index in the input list.
    
    Args:
    nums (list): A list of numbers.
    
    Returns:
    list: A list of the running maxima.
    
    Raises:
    ValueError: If the input list is empty.
    """
    if not nums:
        raise ValueError("Input list cannot be empty.")
    
    result = []
    current_max = float('-inf')
    for num in nums:
        current_max = max(current_max, num)
        result.append(current_max)
    return result
```
```

**style_text** — content=0.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def running_max(nums: list) -> list:
    """
    Returns a list where each element is the running maximum up to that index in nums.
    
    Args:
    nums (list): A list of numbers.
    
    Returns:
    list: A list of the running maxima.
    
    Raises:
    ValueError: If the input list is empty.
    """
    if not nums:
        raise ValueError("Input list cannot be empty.")
    result = []
    current_max = float('-inf')
    for num in nums:
        current_max = max(current_max, num)
        result.append(current_max)
    return result
```
```

**primed** — content=0.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def running_max(nums: list) -> list:
    """
    Returns a list where each element is the running maximum up to that index in the input list.
    
    Args:
    nums (list): A list of numbers.
    
    Returns:
    list: A list of the running maxima.
    
    Raises:
    ValueError: If the input list is empty.
    """
    if not nums:
        raise ValueError("Input list cannot be empty.")
    
    result = []
    current_max = float('-inf')
    for num in nums:
        current_max = max(current_max, num)
        result.append(current_max)
    return result
```
```

### average

> Write a function `average(nums: list) -> float` returning the arithmetic mean of the numbers.

**zero_shot** — content=1.00 conformance=0.50 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=x)

```
```python
def average(nums: list) -> float:
    return sum(nums) / len(nums)
```
```

**full** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def average(nums: list) -> float:
    """
    Return the arithmetic mean of the numbers in nums.
    """
    if not isinstance(nums, list) or not all(isinstance(x, (int, float)) for x in nums):
        raise ValueError("nums must be a list of numbers")
    return sum(nums) / len(nums)
```
```

**compressed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def average(nums: list) -> float:
    """
    Calculate the arithmetic mean of a list of numbers.

    Args:
    nums (list): A list of numbers.

    Returns:
    float: The arithmetic mean of the numbers.
    
    Raises:
    ValueError: If the input list is empty.
    """
    if not nums:
        raise ValueError("The list of numbers cannot be empty.")
    return sum(nums) / len(nums)
```
```

**style_text** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def average(nums: list) -> float:
    """
    Calculate the arithmetic mean of the numbers in nums.
    
    Args:
    nums (list): A list of numbers.
    
    Returns:
    float: The arithmetic mean of the numbers.
    
    Raises:
    ValueError: If nums is empty.
    """
    if not nums:
        raise ValueError("The list of numbers is empty.")
    return sum(nums) / len(nums)
```
```

**primed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def average(nums: list) -> float:
    """
    Calculate the arithmetic mean of a list of numbers.

    Args:
    nums (list): A list of numbers.

    Returns:
    float: The arithmetic mean of the numbers.
    
    Raises:
    ValueError: If the input list is empty.
    """
    if not nums:
        raise ValueError("Input list cannot be empty.")
    return sum(nums) / len(nums)
```
```

### flatten

> Write a function `flatten(matrix: list) -> list` that concatenates a list of lists into one flat list.

**zero_shot** — content=1.00 conformance=0.50 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=x)

```
```python
def flatten(matrix: list) -> list:
    return [item for sublist in matrix for item in sublist]
```
```

**full** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def flatten(matrix: list) -> list:
    """
    Flatten a list of lists into a single list.
    
    Args:
    matrix (list): A list of lists to be flattened.
    
    Returns:
    list: A single list containing all elements of the input lists.
    
    Raises:
    ValueError: If the input is not a list of lists.
    """
    if not all(isinstance(row, list) for row in matrix):
        raise ValueError("Input must be a list of lists.")
    return [item for sublist in matrix for item in sublist]
```
```

**compressed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def flatten(matrix: list) -> list:
    """
    Flattens a matrix (list of lists) into a single list.
    
    Args:
    matrix (list): A list of lists to be flattened.
    
    Returns:
    list: A single list containing all elements from the sublists.
    
    Raises:
    ValueError: If the input is not a list of lists.
    """
    if not all(isinstance(row, list) for row in matrix):
        raise ValueError("Input must be a list of lists.")
    
    return [item for sublist in matrix for item in sublist]
```
```

**style_text** — content=0.00 conformance=0.00 (snake_case=x, type_hints=x, raises_valueerror=x, docstring=x)

```
```python
def flatten(matrix: list) -> list:
    """
    Flattens a nested list into a single list.
    
    Args:
    matrix (list): A list of lists to be flattened.
    
    Returns:
    list: A single flattened list containing all elements of the input lists.
    
    Raises:
    ValueError: If the input is not a list of lists.
    """
    if not all(isinstance sublist, list for sublist in matrix):
        raise ValueError("Input must be a list of lists.")
    return [item for sublist in matrix for item in sublist]
```
```

**primed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def flatten(matrix: list) -> list:
    """
    Flattens a multi-dimensional list (matrix) into a single-dimensional list.
    
    Args:
    matrix (list): A list of lists to be flattened.
    
    Returns:
    list: A flat list containing all elements from the sublists.
    
    Raises:
    ValueError: If the input is not a list of lists.
    """
    if not all(isinstance(row, list) for row in matrix):
        raise ValueError("Input must be a list of lists.")
    
    return [item for sublist in matrix for item in sublist]
```
```

## Domain: math (full conformance=0.85 -> PASS)

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| zero_shot | 1.00 | 0.10 +/-0.14 | 57 |
| full | 1.00 | 0.85 +/-0.14 | 223 |
| compressed | 1.00 | 0.40 +/-0.22 | 85 |
| style_text | 1.00 | 0.75 +/-0.00 | 128 |
| primed | 1.00 | 0.40 +/-0.22 | 85 |

### pages_left

> A book has 120 pages. Ada read 45 pages on Monday and 35 on Tuesday. How many pages are left?

**zero_shot** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=PASS, answer_line=x, no_prose_intro=x)

```
To find out how many pages are left for Ada to read, we need to subtract the number of pages she has already read from the total number of pages in the book.

The total number of pages in the book is 120.

Pages read on Monday: 45
Pages read on Tuesday: 35

Total pages read = Pages read on Monday + Pages read on Tuesday
                 = 45 + 35
                 = 80

Now, subtract the total pages read from the total number of pages in the book:

Pages left = Total pages - Total pages read
           = 120 - 80
           = 40

So, there are 40 pages left for Ada to read.
```

**full** — content=1.00 conformance=1.00 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate total pages read on Monday and Tuesday.
   - Pages read on Monday: 45
   - Pages read on Tuesday: 35
   - Total pages read = 45 + 35 = 80

Step 2: Subtract the total pages read from the total pages in the book to find out how many pages are left.
   - Total pages in the book: 120
   - Pages left = 120 - 80 = 40

Answer: 40
```

**compressed** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=x)

```
To find out how many pages are left for Ada to read, we need to follow these steps:

1. Calculate the total number of pages Ada has already read.
2. Subtract the total number of pages read from the initial number of pages in the book.

Step 1: Calculate the total number of pages Ada has already read.
- Pages read on Monday: 45
- Pages read on Tuesday: 35

Total pages read = Pages read on Monday + Pages read on Tuesday
Total pages read = 45 + 35
Total pages read = 80

Step 2: Subtract the total number of pages read from the initial number of pages in the book.
- Initial number of pages in the book: 120
- Total pages read: 80

Pages left = Initial number of pages - Total pages read
Pages left = 120 - 80
Pages left = 40

Answer: 40
```

**style_text** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=x, no_prose_intro=PASS)

```
Step 1: Determine the total number of pages Ada has read.
- Pages read on Monday: 45
- Pages read on Tuesday: 35

Total pages read = 45 + 35

Step 2: Perform the addition from Step 1.
- Total pages read = 45 + 35 = 80

Step 3: Subtract the total pages read from the total number of pages in the book to find out how many pages are left.
- Total pages in the book: 120
- Total pages read: 80

Pages left = 120 - 80

Step 4: Perform the subtraction from Step 3.
- Pages left = 120 - 80 = 40

Final Answer: 40
```

**primed** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=x)

```
To find out how many pages are left for Ada to read, we need to follow these steps:

1. Calculate the total number of pages Ada has already read.
2. Subtract the total number of pages she has already read from the total number of pages in the book.

Step 1: Calculate the total number of pages Ada has already read.
- Pages read on Monday: 45
- Pages read on Tuesday: 35

Total pages read = Pages read on Monday + Pages read on Tuesday
Total pages read = 45 + 35
Total pages read = 80

Step 2: Subtract the total number of pages she has already read from the total number of pages in the book.
- Total pages in the book: 120
- Total pages read: 80

Pages left = Total pages in the book - Total pages read
Pages left = 120 - 80
Pages left = 40

Answer: 40
```

### hen_eggs

> A farmer has 5 hens and each lays 6 eggs. How many eggs in total?

**zero_shot** — content=1.00 conformance=0.00 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=x)

```
To find the total number of eggs laid by the 5 hens, you can multiply the number of hens by the number of eggs each hen lays.

So, if there are 5 hens and each hen lays 6 eggs:

\[ 5 \text{ hens} \times 6 \text{ eggs/hen} = 30 \text{ eggs} \]

Therefore, the total number of eggs laid is 30.
```

**full** — content=1.00 conformance=0.75 (numbered_steps=x, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: multiply number of hens by eggs per hen = 5 * 6 = 30
Answer: 30
```

**compressed** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=x, answer_line=PASS, no_prose_intro=x)

```
To solve this problem, we need to calculate the total number of eggs laid by all the hens.

1. Identify the number of hens: There are 5 hens.
2. Identify the number of eggs each hen lays: Each hen lays 6 eggs.
3. Calculate the total number of eggs by multiplying the number of hens by the number of eggs each hen lays:

\[ \text{Total eggs} = \text{Number of hens} \times \text{Eggs per hen} \]
\[ \text{Total eggs} = 5 \times 6 \]

4. Perform the multiplication:

\[ 5 \times 6 = 30 \]

Therefore, the total number of eggs is 30.

Answer: 30
```

**style_text** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Identify the number of hens and the number of eggs each hen lays.
- Number of hens = 5
- Eggs per hen = 6

Step 2: Calculate the total number of eggs by multiplying the number of hens by the number of eggs each hen lays.
- Total eggs = Number of hens × Eggs per hen
- Total eggs = 5 × 6

Step 3: Perform the multiplication.
- 5 × 6 = 30

Step 4: State the final answer.
Answer: 30
```

**primed** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=x, answer_line=PASS, no_prose_intro=x)

```
To solve this problem, we need to calculate the total number of eggs laid by all the hens.

1. Identify the number of hens: There are 5 hens.
2. Identify the number of eggs each hen lays: Each hen lays 6 eggs.
3. Calculate the total number of eggs by multiplying the number of hens by the number of eggs each hen lays:

\[ \text{Total eggs} = \text{Number of hens} \times \text{Eggs per hen} \]
\[ \text{Total eggs} = 5 \times 6 \]

4. Perform the multiplication:

\[ 5 \times 6 = 30 \]

Therefore, the total number of eggs is 30.

Answer: 30
```

### tank_left

> A tank holds 50 liters. 18 liters are used in the morning and 12 in the evening. How many liters are left?

**zero_shot** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=PASS, answer_line=x, no_prose_intro=x)

```
To find out how many liters are left in the tank, we need to subtract the total amount of water used from the initial amount.

The initial amount of water in the tank is 50 liters.

In the morning, 18 liters are used.
In the evening, 12 liters are used.

So, the total amount of water used is \(18 + 12 = 30\) liters.

Now, subtract the total amount used from the initial amount:

\(50 - 30 = 20\)

Therefore, there are 20 liters left in the tank.
```

**full** — content=1.00 conformance=1.00 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Subtract the liters used in the morning from the total capacity = 50 - 18 = 32 liters
Step 2: Subtract the liters used in the evening from the remaining capacity = 32 - 12 = 20 liters
Answer: 20
```

**compressed** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=x, answer_line=PASS, no_prose_intro=x)

```
To solve this problem, let's break it down into steps:

1. **Initial Volume**: The tank starts with 50 liters of liquid.

2. **Morning Usage**: In the morning, 18 liters are used.
   - To find out how much is left after the morning usage, we subtract the morning usage from the initial volume:
     \[
     50 \text{ liters} - 18 \text{ liters} = 32 \text{ liters}
     \]

3. **Evening Usage**: In the evening, 12 liters are used.
   - To find out how much is left after the evening usage, we subtract the evening usage from the remaining volume after the morning:
     \[
     32 \text{ liters} - 12 \text{ liters} = 20 \text{ liters}
     \]

4. **Final Volume**: After both the morning and evening usages, the tank has 20 liters left.

Answer: 20
```

**style_text** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=x, no_prose_intro=PASS)

```
Step 1: Determine the total amount of water used.
- Water used in the morning: 18 liters
- Water used in the evening: 12 liters
- Total water used = 18 + 12

Step 2: Calculate the total amount of water used.
- Total water used = 18 + 12 = 30 liters

Step 3: Subtract the total water used from the initial amount to find out how much is left.
- Initial amount of water: 50 liters
- Water left = 50 - 30

Step 4: Calculate the amount of water left.
- Water left = 50 - 30 = 20 liters

Final Answer: 20
```

**primed** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=x, answer_line=PASS, no_prose_intro=x)

```
To solve this problem, let's break it down into steps:

1. **Initial Volume**: The tank starts with 50 liters of liquid.

2. **Morning Usage**: In the morning, 18 liters are used.
   - To find out how much is left after the morning usage, we subtract the morning usage from the initial volume:
     \[
     50 \text{ liters} - 18 \text{ liters} = 32 \text{ liters}
     \]

3. **Evening Usage**: In the evening, 12 liters are used.
   - To find out how much is left after the evening usage, we subtract the evening usage from the remaining volume after the morning:
     \[
     32 \text{ liters} - 12 \text{ liters} = 20 \text{ liters}
     \]

4. **Final Volume**: After both the morning and evening usages, the tank has 20 liters left.

Answer: 20
```

### split_bill

> Three friends split a 60 dollar bill equally. How much does each person pay in dollars?

**zero_shot** — content=1.00 conformance=0.00 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=x)

```
To find out how much each person pays, you need to divide the total amount of the bill by the number of people sharing it.

So, you would calculate:

\[ \text{Amount per person} = \frac{\text{Total bill}}{\text{Number of people}} = \frac{60}{3} = 20 \]

Each person pays $20.
```

**full** — content=1.00 conformance=0.75 (numbered_steps=x, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: divide total amount by number of friends to find out how much each person pays = 60 / 3 = 20
Answer: 20
```

**compressed** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=x, answer_line=PASS, no_prose_intro=x)

```
To solve this problem, we need to divide the total amount of money by the number of people sharing it.

1. The total amount of money is $60.
2. There are 3 friends splitting the bill equally.
3. To find out how much each person pays, we divide $60 by 3.

\[ \text{Amount per person} = \frac{\$60}{3} \]

4. Performing the division:

\[ \frac{\$60}{3} = \$20 \]

Answer: 20
```

**style_text** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Determine how many people are splitting the bill.
There are 3 friends.

Step 2: Calculate the total amount to be split.
The total amount is $60.

Step 3: Divide the total amount by the number of people to find out how much each person pays.
\[ \text{Amount per person} = \frac{\$60}{3} \]

Step 4: Perform the division.
\[ \frac{\$60}{3} = \$20 \]

Step 5: State the final answer.
Answer: 20
```

**primed** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=x, answer_line=PASS, no_prose_intro=x)

```
To solve this problem, we need to divide the total amount of money by the number of people sharing it.

1. The total amount of money is $60.
2. There are 3 friends splitting the bill equally.
3. To find out how much each person pays, we divide $60 by 3.

\[ \text{Amount per person} = \frac{\$60}{3} \]

4. Performing the division:

\[ \frac{\$60}{3} = \$20 \]

Answer: 20
```

### weekly_run

> A runner runs 8 km each day for 5 days. How many km in total?

**zero_shot** — content=1.00 conformance=0.00 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=x)

```
To find the total distance the runner has covered over 5 days, you simply multiply the daily distance by the number of days.

So, if the runner runs 8 km each day for 5 days:

\[ \text{Total Distance} = 8 \, \text{km/day} \times 5 \, \text{days} = 40 \, \text{km} \]

Therefore, the total distance covered is 40 km.
```

**full** — content=1.00 conformance=0.75 (numbered_steps=x, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: multiply daily distance by number of days = 8 * 5 = 40
Answer: 40
```

**compressed** — content=1.00 conformance=0.50 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=x)

```
To find out the total distance the runner covers over 5 days, we need to multiply the daily distance by the number of days.

Step 1: Identify the daily distance.
Daily distance = 8 km

Step 2: Identify the number of days.
Number of days = 5

Step 3: Multiply the daily distance by the number of days.
Total distance = Daily distance × Number of days
Total distance = 8 km/day × 5 days

Step 4: Perform the multiplication.
Total distance = 40 km

Therefore, the total distance covered by the runner over 5 days is 40 km.

Answer: 40
```

**style_text** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Identify the distance run each day and the number of days.
- Distance per day = 8 km
- Number of days = 5

Step 2: Calculate the total distance by multiplying the daily distance by the number of days.
- Total distance = Distance per day × Number of days
- Total distance = 8 km/day × 5 days

Step 3: Perform the multiplication.
- Total distance = 40 km

Step 4: State the final answer.
Answer: 40
```

**primed** — content=1.00 conformance=0.50 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=x)

```
To find out the total distance the runner covers over 5 days, we need to multiply the daily distance by the number of days.

Step 1: Identify the daily distance.
Daily distance = 8 km

Step 2: Identify the number of days.
Number of days = 5

Step 3: Multiply the daily distance by the number of days.
Total distance = Daily distance × Number of days
Total distance = 8 km/day × 5 days

Step 4: Perform the multiplication.
Total distance = 40 km

Therefore, the total distance covered by the runner over 5 days is 40 km.

Answer: 40
```

## Domain: writing (full conformance=0.87 -> PASS)

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| zero_shot | 1.00 | 0.13 +/-0.18 | 41 |
| full | 1.00 | 0.87 +/-0.18 | 150 |
| compressed | 1.00 | 0.33 +/-0.33 | 80 |
| style_text | 0.93 | 0.67 +/-0.24 | 126 |
| primed | 1.00 | 0.40 +/-0.15 | 80 |

### gravity

> Explain what gravity is.

**zero_shot** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Gravity is a fundamental force of nature that attracts two bodies with mass towards each other. It is one of the four fundamental forces in the universe, alongside electromagnetism, the strong nuclear force, and the weak nuclear force. Gravity acts on all objects with mass or energy, regardless of their size or composition.

In the simplest terms, gravity is described by Newton's law of universal gravitation, which states that every particle attracts every other particle in the universe with a force that is directly proportional to the product of their masses and inversely proportional to the square of the distance between their centers. This means that the more massive an object is, and the closer it is to another object, the stronger the gravitational pull between them.

Albert Einstein provided a more comprehensive understanding of gravity through his theory of general relativity. According to this theory, massive objects cause a distortion in the fabric of spacetime around them, and this curvature affects the motion of other objects. Essentially, gravity can be thought of as the effect of this curvature on the paths that objects follow through space and time.

In everyday life, we experience gravity as the force that pulls us down when we jump or causes planets to orbit stars. Gravity plays a crucial role in shaping the structure of our universe, influencing the formation of galaxies, stars, and even black holes.
```

**full** — content=1.00 conformance=0.67 (second_person=x, no_contractions=PASS, bulleted_list=PASS)

```
- Gravity is a force that attracts two objects with mass towards each other.
- This force is responsible for keeping planets in orbit around the sun and for making objects on Earth stay on the ground.
- The strength of gravity depends on the masses of the objects and the distance between them.
```

**compressed** — content=1.00 conformance=0.33 (second_person=PASS, no_contractions=x, bulleted_list=x)

```
Certainly! Gravity is a fundamental force of nature that attracts two bodies with mass towards each other. Imagine you have a ball and a feather. If you drop them both from the same height at the same time, they will hit the ground at the same time because the gravitational pull on both objects is the same. This universal attraction between masses is what we call gravity. It's what keeps us grounded and allows planets to orbit stars. Gravity works on all scales—from the tiny scale of subatomic particles to the vast scale of galaxies.
```

**style_text** — content=1.00 conformance=0.67 (second_person=x, no_contractions=PASS, bulleted_list=PASS)

```
Explain what gravity is.

- Gravity is a force that attracts objects towards each other.
- It is caused by the mass of an object; more massive objects have a stronger gravitational pull.
- This force allows planets to orbit stars and keeps us grounded on Earth.
```

**primed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Gravity is a force that attracts two objects with mass towards each other. It is always present and acts in all directions. The strength of this attraction depends on the masses of the objects and the distance between them. The greater the mass of an object, the stronger its gravitational pull. As for the distance, the effect of gravity weakens rapidly as the distance between objects increases.
```

### vaccine

> Explain what a vaccine does.

**zero_shot** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
A vaccine is a biological preparation that helps to build the immunity to a particular disease. It works by stimulating the body's immune system to recognize and fight off specific pathogens, such as viruses or bacteria, without actually causing the disease.

Here’s how it typically works:

1. **Introduction of Pathogen Components**: Vaccines contain weakened or inactivated forms of pathogens, or pieces of these pathogens (like proteins or sugars). These components trigger an immune response in the body.

2. **Immune Response**: When the body encounters these components, it produces antibodies and memory cells. Antibodies are proteins that can recognize and bind to specific pathogens, while memory cells remember how to respond if the same pathogen is encountered again.

3. **Memory Cells**: The memory cells remain in the body after the initial infection has been cleared. If the actual pathogen enters the body later, these memory cells can quickly produce antibodies to neutralize the pathogen before it causes illness.

4. **Prevention of Disease**: By preparing the immune system in advance, vaccines prevent or reduce the severity of diseases caused by those pathogens. This means that even if someone is exposed to the real pathogen, their immune system is already prepared to fight it off.

Vaccines have been instrumental in eradicating or significantly reducing the impact of many diseases, including smallpox, polio, measles, and others. They are one of the most effective tools we have for preventing infectious diseases and saving lives.
```

**full** — content=1.00 conformance=1.00 (second_person=PASS, no_contractions=PASS, bulleted_list=PASS)

```
- A vaccine introduces a small part of a germ or a weakened version of a germ into your body.
- This causes your immune system to recognize and fight off the germ without getting sick.
- Your immune system then remembers how to fight that specific germ if you are exposed to it later.
- This helps protect you from getting sick with diseases that vaccines prevent.
```

**compressed** — content=1.00 conformance=0.67 (second_person=PASS, no_contractions=PASS, bulleted_list=x)

```
Sure! Here’s how you can address the reader directly and explain what a vaccine does:

---

Hello,

A vaccine works by introducing a small part of a germ, like a virus or bacteria, into your body. This triggers your immune system to create antibodies without actually making you sick. Over time, your body remembers this germ and knows how to fight it if you ever encounter the real thing. This way, vaccines help protect you from getting sick with certain diseases.

---

I hope this helps!
```

**style_text** — content=0.67 conformance=1.00 (second_person=PASS, no_contractions=PASS, bulleted_list=PASS)

```
Explain what a vaccine does.

- A vaccine introduces a small part of a germ or a weakened version of it into your body.
- This causes your immune system to recognize and remember that germ.
- Your immune system then produces antibodies to fight off the germ if you are exposed to it later.
- The antibodies help protect your body from getting sick when you encounter the real germ.
```

**primed** — content=1.00 conformance=0.67 (second_person=PASS, no_contractions=PASS, bulleted_list=x)

```
Certainly! Here’s how you can address the reader directly while explaining what a vaccine does:

Addressing the Reader Directly:
Explaining What a Vaccine Does:

A vaccine introduces substances that mimic an infection without causing the disease itself. These substances, often proteins or sugars from the pathogen, trigger your immune system to produce antibodies and memory cells. This prepares your body to recognize and fight off the actual pathogen if you encounter it in the future. Over time, these defenses help protect you from getting sick again.
```

### tides

> Explain what causes ocean tides.

**zero_shot** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Ocean tides are primarily caused by the gravitational pull of the Moon and, to a lesser extent, the Sun on Earth's oceans. The gravitational force exerted by these celestial bodies pulls water towards them, creating high tides on the side of Earth closest to the Moon and on the opposite side, where the Moon is farthest away. This phenomenon is known as the "tidal bulge."

However, the Earth is not a perfect sphere; it is slightly flattened at the poles and bulged at the equator due to its rotation. This effect, combined with the gravitational pull from the Sun, creates a more complex tidal pattern. When the Sun, Earth, and Moon are aligned (during full moon or new moon), their combined gravitational forces create higher than average tides called spring tides. Conversely, when the Sun and Moon are at right angles to each other relative to Earth (during quarter moons), their gravitational forces partially cancel each other out, resulting in lower than average tides called neap tides.

Additionally, the Earth's rotation and the shape of the coastline also play roles in shaping the patterns of ocean tides. Coastal areas can experience different tidal patterns depending on the local geography, such as estuaries, bays, and harbors, which can affect the timing and height of the tides.
```

**full** — content=1.00 conformance=0.67 (second_person=PASS, no_contractions=x, bulleted_list=PASS)

```
- You can consider the causes of ocean tides as primarily due to the gravitational pull exerted by the moon and, to a lesser extent, the sun.
- The moon's gravity creates two bulges in the Earth's oceans, one on the side facing the moon and another on the opposite side.
- Additionally, the sun's gravity also contributes to this effect, but its influence is about half that of the moon.
- These gravitational forces cause the water to be pulled towards them, creating high tides, while the rest of the water is pulled away, resulting in low tides.
```

**compressed** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Certainly! Let's address the reader directly:

Explaining what causes ocean tides:

The ocean tides are primarily caused by the gravitational pull of the Moon and, to a lesser extent, the Sun on Earth. As the Moon orbits around Earth, its gravity pulls on the water in the oceans, creating high and low tides. This effect is stronger near the Moon because the Moon's gravity exerts a stronger pull on water closer to it. The Sun also contributes to tides, but its influence is about half that of the Moon due to its greater distance from Earth.

As the Earth rotates, different parts of the planet experience these tidal forces at various times, leading to the rise and fall of sea levels we call tides. The exact timing and height of tides can vary depending on the position of the Moon and Sun relative to Earth, as well as the shape of the coastline and the depth of the ocean.
```

**style_text** — content=1.00 conformance=0.33 (second_person=x, no_contractions=x, bulleted_list=PASS)

```
Explain what causes ocean tides.

- The gravitational pull of the moon and, to a lesser extent, the sun, cause the water on Earth's surface to bulge out in two areas.
- As the moon orbits the Earth, its gravity pulls on the water, creating high tides on the side of the Earth closest to it and on the opposite side.
- The sun also exerts a gravitational pull, but because it is much farther away from the Earth, this effect is less noticeable than the moon's.
- This combined gravitational force causes the water to rise and fall, creating the cycle of high and low tides that we observe.
```

**primed** — content=1.00 conformance=0.33 (second_person=PASS, no_contractions=x, bulleted_list=x)

```
Certainly! Here's how you can address the reader directly while explaining what causes ocean tides:

Addressing the Reader Directly:
Explaining What Causes Ocean Tides

Evaporation is liquid turning into gas.
Molecules gain energy to leave surface.
Speeds up with higher temperatures.

Now, for the explanation of ocean tides:

The ocean tides are primarily caused by the gravitational pull of the Moon and, to a lesser extent, the Sun on Earth. As the Moon orbits around Earth, it exerts a gravitational force on the water, causing it to bulge out in the direction of the Moon. This creates high tides on one side of Earth. At the same time, the opposite side experiences a low tide due to the absence of the Moon's gravitational influence. The Sun also contributes to this effect, but its gravitational pull is slightly weaker than that of the Moon. Therefore, during new and full moons when the Sun, Earth, and Moon are aligned, their combined gravitational forces create higher high tides and lower low tides, known as spring tides. In between these times, the gravitational effects of the Sun and Moon work together less effectively, resulting in smaller tidal variations called neap tides.
```

### friction

> Explain what friction is.

**zero_shot** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Friction is a force that resists the relative motion of objects sliding against each other. It occurs between two surfaces in contact and acts parallel to the surface of contact, opposite to the direction of the applied force. Friction plays a crucial role in many aspects of our daily lives and in various technological applications.

There are different types of friction, including static friction (the force that prevents an object from starting to move when a force is applied) and kinetic friction (the force that acts on an object once it is moving). The coefficient of friction is a dimensionless number that characterizes the ratio of the force of friction between two bodies and the normal force pressing them together.

Understanding friction is important because it affects how objects move and interact with their environment. Engineers and designers must consider friction when creating products or systems to ensure they function as intended. For example, reducing friction can improve the efficiency of machines, while increasing friction can enhance grip and stability.
```

**full** — content=1.00 conformance=1.00 (second_person=PASS, no_contractions=PASS, bulleted_list=PASS)

```
- Friction is the force that resists the relative motion of objects sliding against each other.
- It occurs between surfaces in contact and depends on the nature of the surfaces and how rough they are.
- You can observe friction when you try to slide a book across a table; it does not move easily because of friction between the book and the table.
```

**compressed** — content=1.00 conformance=0.67 (second_person=x, no_contractions=PASS, bulleted_list=PASS)

```
Certainly! Friction is the force that resists the relative motion of objects sliding against each other. To explain it in a simple way:

- Friction occurs when two surfaces come into contact.
- It arises due to the irregularities on the surfaces that get interlocked as they move.
- The more rough or uneven the surfaces are, the greater the friction will be.
- Friction can slow down or stop moving objects and is important for many everyday activities like walking or driving a car.
```

**style_text** — content=1.00 conformance=0.67 (second_person=x, no_contractions=PASS, bulleted_list=PASS)

```
Explain what friction is.

- Friction is a force that resists the relative motion of objects sliding against each other.
- It occurs between surfaces in contact.
- Friction depends on the nature of the surfaces and their roughness.
```

**primed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Friction is the force that resists the relative motion of objects sliding or rolling against each other. When two surfaces come into contact and move in different directions, the molecules on the surfaces resist this movement, creating friction. The strength of this resistance depends on the nature of the surfaces in contact and their smoothness. Higher temperatures can increase the kinetic energy of the molecules, making them more active and thus increasing the friction.
```

### evaporation

> Explain what evaporation is.

**zero_shot** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Evaporation is the process by which liquid turns into vapor or gas directly at the surface of a liquid, without passing through the solid state. This process occurs when molecules with higher energy escape from the liquid and enter the surrounding air as a gas. The rate of evaporation depends on factors such as temperature (higher temperatures increase the rate), surface area (larger areas allow more molecules to escape), and humidity (drier conditions increase the rate).

Evaporation is an important part of the water cycle, where it contributes to the formation of clouds and precipitation. It also plays a role in cooling systems, such as evaporative coolers, which work by allowing water to evaporate and take heat away from the air.
```

**full** — content=1.00 conformance=1.00 (second_person=PASS, no_contractions=PASS, bulleted_list=PASS)

```
Explain what evaporation is.

- You can think of evaporation as the process where a liquid transforms into a gas.
- This occurs when individual molecules within the liquid acquire sufficient kinetic energy to overcome the intermolecular forces holding them in the liquid state.
- As the temperature increases, more molecules have the necessary energy to escape into the air, thus accelerating the rate of evaporation.
```

**compressed** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Sure! Here's a short explanation of evaporation:

Evaporation is the process where liquid turns into vapor or gas. This happens when molecules at the surface of a liquid gain enough energy to break free from the liquid and enter the air as a gas. The rate of evaporation increases with higher temperatures because more molecules have the necessary energy to escape the liquid's surface.
```

**style_text** — content=1.00 conformance=0.67 (second_person=x, no_contractions=PASS, bulleted_list=PASS)

```
Explain what evaporation is.

- Evaporation is liquid turning into gas.
- Molecules gain energy to leave the surface.
- The process speeds up with higher temperatures.
```

**primed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Evaporation is the process where liquid turns into gas. As molecules gain energy, they move faster and eventually break free from the surface of the liquid, turning into gas. This process speeds up as the temperature increases.
```
