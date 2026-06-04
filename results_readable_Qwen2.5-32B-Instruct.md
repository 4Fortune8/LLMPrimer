# Primer harness run (Qwen/Qwen2.5-32B-Instruct, split=test, seeds=[0], regime=compressed)

## Overall

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| zero_shot | 0.93 | 0.21 +/-0.24 | 53 |
| full | 0.98 | 0.91 +/-0.13 | 203 |
| compressed | 0.93 | 0.61 +/-0.38 | 110 |
| style_text | 0.93 | 0.91 +/-0.14 | 154 |
| primed | 1.00 | 0.61 +/-0.38 | 110 |

## Value (cost-adjusted: primer vs re-pasted text rival)

| scope | conf gain vs compressed | conf vs style_text | tokens vs style_text | verdict |
|---|---|---|---|---|
| coding | +0.00 | -0.05 | -43 | mixed (trade-off) |
| math | +0.00 | -0.10 | -43 | mixed (trade-off) |
| writing | +0.00 | -0.73 | -46 | mixed (trade-off) |
| **gated overall** | +0.00 | -0.29 | -44 | mixed (trade-off) |

## Domain: coding (full conformance=0.95 -> PASS)

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| zero_shot | 1.00 | 0.50 +/-0.00 | 61 |
| full | 1.00 | 0.95 +/-0.11 | 235 |
| compressed | 0.80 | 0.95 +/-0.11 | 104 |
| style_text | 0.80 | 1.00 +/-0.00 | 147 |
| primed | 1.00 | 0.95 +/-0.11 | 104 |

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
            result.append(item)
            seen.add(item)
    return result
```
```

**full** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
def dedupe(items: list) -> list:
    """Remove duplicates from items while preserving order."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result
```
```

**compressed** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
def dedupe(items: list) -> list:
    """
    Remove duplicates from a list while preserving the order of first occurrences.

    :param items: List of items to process.
    :type items: list
    :return: A new list with duplicates removed, preserving the original order.
    :rtype: list
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result
```
```

**style_text** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def dedupe(items: list) -> list:
    """
    Remove duplicates from a list while preserving the order of first occurrences.
    
    :param items: List of items to process.
    :type items: list
    :return: A new list with duplicates removed, preserving the original order.
    :rtype: list
    :raises ValueError: If the input is not a list.
    """
    if not isinstance(items, list):
        raise ValueError("Input must be a list.")
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result
```
```

**primed** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
def dedupe(items: list) -> list:
    """
    Remove duplicates from a list while preserving the order of first occurrences.

    :param items: List of items to process.
    :type items: list
    :return: A new list with duplicates removed, preserving the original order.
    :rtype: list
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result
```
```

### word_frequencies

> Write a function `word_freq(text: str) -> dict` mapping each lowercased word to its count.

**zero_shot** — content=1.00 conformance=0.50 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=x)

```
```python
def word_freq(text: str) -> dict:
    words = text.lower().split()
    freq_dict = {}
    for word in words:
        if word in freq_dict:
            freq_dict[word] += 1
        else:
            freq_dict[word] = 1
    return freq_dict
```
```

**full** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def word_freq(text: str) -> dict:
    """Return a dictionary mapping each lowercased word to its frequency in text."""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    words = text.lower().split()
    freq_dict = {}
    for word in words:
        if word.isalpha():
            freq_dict[word] = freq_dict.get(word, 0) + 1
    return freq_dict
```
```

**compressed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def word_freq(text: str) -> dict:
    """
    Returns a dictionary mapping each lowercased word to its frequency in the given text.

    :param text: The input string from which to count word frequencies.
    :return: A dictionary with words as keys and their counts as values.
    :raises ValueError: If the input is not a string.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    words = text.lower().split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq
```
```

**style_text** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def word_freq(text: str) -> dict:
    """
    Returns a dictionary mapping each lowercased word to its frequency in the text.
    
    :param text: The input text string.
    :return: A dictionary with words as keys and their counts as values.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    words = text.lower().split()
    freq = {}
    for word in words:
        if word.isalpha():
            freq[word] = freq.get(word, 0) + 1
    return freq
```
```

**primed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def word_freq(text: str) -> dict:
    """
    Returns a dictionary mapping each lowercased word to its frequency in the given text.

    :param text: The input string containing words.
    :return: A dictionary with keys as words (lowercased) and values as their counts.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    
    words = text.split()
    freq_dict = {}
    for word in words:
        lower_word = word.lower()
        if lower_word in freq_dict:
            freq_dict[lower_word] += 1
        else:
            freq_dict[lower_word] = 1
    return freq_dict
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
    max_val = nums[0]
    result = []
    for num in nums:
        max_val = max(max_val, num)
        result.append(max_val)
    return result
```
```

**full** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def running_max(nums: list[int]) -> list[int]:
    """Return a list where each element is the maximum up to that index in nums."""
    if not all(isinstance(x, int) for x in nums):
        raise ValueError("All elements in nums must be integers")
    max_list = []
    current_max = nums[0] if nums else None
    for num in nums:
        if current_max is None or num > current_max:
            current_max = num
        max_list.append(current_max)
    return max_list
```
```

**compressed** — content=0.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def running_max(nums: list) -> list:
    """
    Returns a list where each element is the maximum value found up to that point in the input list.

    :param nums: List of integers.
    :return: A list of integers representing the cumulative maximums.
    :raises ValueError: If the input list is empty.
    """
    if not nums:
        raise ValueError("Input list cannot be empty")
    
    max_val = nums[0]
    result = []
    for num in nums:
        max_val = max(max_val, num)
        result.append(max_val)
    return result
```
```

**style_text** — content=0.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def running_max(nums: list[int]) -> list[int]:
    """
    Returns a list where each element is the maximum value found up to that point in the input list.
    
    Args:
        nums (list[int]): List of integers.

    Returns:
        list[int]: List of cumulative maximums.
    
    Raises:
        ValueError: If the input list is empty.
    """
    if not nums:
        raise ValueError("Input list cannot be empty")
    max_list = [nums[0]]
    for num in nums[1:]:
        max_list.append(max(max_list[-1], num))
    return max_list
```
```

**primed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def running_max(nums: list) -> list:
    """
    Returns a list where each element is the maximum value found up to that point in the input list.

    :param nums: List of integers.
    :return: A list of cumulative maximums.
    """
    if not all(isinstance(x, int) for x in nums):
        raise ValueError("All elements in the list must be integers.")
    
    max_list = []
    current_max = float('-inf')
    for num in nums:
        if num > current_max:
            current_max = num
        max_list.append(current_max)
    return max_list
```
```

### average

> Write a function `average(nums: list) -> float` returning the arithmetic mean of the numbers.

**zero_shot** — content=1.00 conformance=0.50 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=x)

```
```python
def average(nums: list) -> float:
    if not nums:
        return 0.0
    return sum(nums) / len(nums)
```
```

**full** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def average(nums: list[float]) -> float:
    """Calculate the arithmetic mean of the numbers in nums."""
    if not nums:
        raise ValueError("nums cannot be an empty list")
    return sum(nums) / len(nums)
```
```

**compressed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def average(nums: list) -> float:
    """
    Calculate the arithmetic mean of a list of numbers.

    :param nums: List of numbers to calculate the mean.
    :return: The arithmetic mean as a float.
    :raises ValueError: if the input list is empty.
    """
    if not nums:
        raise ValueError("Input list must not be empty.")
    return sum(nums) / len(nums)
```
```

**style_text** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def average(nums: list[float]) -> float:
    """
    Returns the arithmetic mean of the numbers.

    :param nums: List of numbers to calculate the mean.
    :return: The arithmetic mean as a float.
    :raises ValueError: if the input list is empty.
    """
    if not nums:
        raise ValueError("The input list must not be empty.")
    return sum(nums) / len(nums)
```
```

**primed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def average(nums: list) -> float:
    """
    Calculate the arithmetic mean of a list of numbers.

    :param nums: List of numbers to calculate the mean.
    :return: The arithmetic mean as a float.
    :raises ValueError: If the input list is empty.
    """
    if not nums:
        raise ValueError("Input list must not be empty.")
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
    """Concatenate a list of lists into one flat list."""
    if not all(isinstance(row, list) for row in matrix):
        raise ValueError("All elements of the matrix must be lists")
    return [item for sublist in matrix for item in sublist]
```
```

**compressed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def flatten(matrix: list) -> list:
    """
    Flattens a list of lists into a single list.

    :param matrix: List of lists to be flattened.
    :type matrix: list
    :return: A single list containing all elements from the sublists.
    :rtype: list
    :raises ValueError: If the input is not a list of lists.
    """
    if not all(isinstance(sublist, list) for sublist in matrix):
        raise ValueError("Input must be a list of lists")
    return [element for sublist in matrix for element in sublist]
```
```

**style_text** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def flatten(matrix: list[list]) -> list:
    """
    Concatenates a list of lists into one flat list.
    
    Args:
        matrix (list[list]): A list of lists to be flattened.

    Returns:
        list: A single list containing all the elements of the nested lists.

    Raises:
        ValueError: If the input is not a list of lists.
    """
    if not all(isinstance(item, list) for item in matrix):
        raise ValueError("Input must be a list of lists.")
    return [element for sublist in matrix for element in sublist]
```
```

**primed** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def flatten(matrix: list) -> list:
    """
    Flattens a list of lists into a single list.

    :param matrix: List of lists to be flattened.
    :type matrix: list
    :return: A single list containing all elements from the sublists.
    :rtype: list
    :raises ValueError: If the input is not a list of lists.
    """
    if not all(isinstance(sublist, list) for sublist in matrix):
        raise ValueError("Input must be a list of lists")
    return [element for sublist in matrix for element in sublist]
```
```

## Domain: math (full conformance=0.85 -> PASS)

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| zero_shot | 0.80 | 0.05 +/-0.11 | 57 |
| full | 1.00 | 0.85 +/-0.14 | 223 |
| compressed | 1.00 | 0.75 +/-0.00 | 120 |
| style_text | 1.00 | 0.85 +/-0.14 | 163 |
| primed | 1.00 | 0.75 +/-0.00 | 120 |

### pages_left

> A book has 120 pages. Ada read 45 pages on Monday and 35 on Tuesday. How many pages are left?

**zero_shot** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=PASS, answer_line=x, no_prose_intro=x)

```
To find out how many pages are left for Ada to read, we need to subtract the number of pages she has already read from the total number of pages in the book.

The total number of pages in the book is 120.

Ada read 45 pages on Monday and 35 pages on Tuesday, so the total number of pages she has read is:

\[ 45 + 35 = 80 \]

Now, subtract the number of pages Ada has read from the total number of pages:

\[ 120 - 80 = 40 \]

So, Ada has 40 pages left to read.
```

**full** — content=1.00 conformance=1.00 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate total pages read = 45 + 35 = 80
Step 2: Subtract pages read from total pages = 120 - 80 = 40
Answer: 40
```

**compressed** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total number of pages Ada read.
45 (Monday) + 35 (Tuesday) = 80 pages

Step 2: Subtract the total number of pages Ada read from the total number of pages in the book.
120 (total pages) - 80 (pages read) = 40 pages

Answer: 40
```

**style_text** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total number of pages Ada read on Monday and Tuesday.
        45 (Monday) + 35 (Tuesday) = 80 pages
Step 2: Subtract the total number of pages Ada read from the total number of pages in the book.
        120 (total pages) - 80 (pages read) = 40 pages
Answer: 40
```

**primed** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total number of pages Ada read.
45 (Monday) + 35 (Tuesday) = 80 pages

Step 2: Subtract the total number of pages Ada read from the total number of pages in the book.
120 (total pages) - 80 (pages read) = 40 pages

Answer: 40
```

### hen_eggs

> A farmer has 5 hens and each lays 6 eggs. How many eggs in total?

**zero_shot** — content=1.00 conformance=0.00 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=x)

```
To find the total number of eggs, you multiply the number of hens by the number of eggs each hen lays.

Given:
- Number of hens = 5
- Eggs per hen = 6

Total number of eggs = Number of hens × Eggs per hen
Total number of eggs = 5 × 6
Total number of eggs = 30

So, the total number of eggs is 30.
```

**full** — content=1.00 conformance=0.75 (numbered_steps=x, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: multiply number of hens by eggs per hen = 5 * 6 = 30
Answer: 30
```

**compressed** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total number of eggs by multiplying the number of hens by the number of eggs each hen lays.
Step 2: 5 hens * 6 eggs/hen = 30 eggs.
Answer: 30.
```

**style_text** — content=1.00 conformance=1.00 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total number of eggs by multiplying the number of hens by the number of eggs each hen lays.
Step 2: 5 * 6 = 30
Answer: 30
```

**primed** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total number of eggs by multiplying the number of hens by the number of eggs each hen lays.
Step 2: 5 hens * 6 eggs/hen = 30 eggs.
Answer: 30.
```

### tank_left

> A tank holds 50 liters. 18 liters are used in the morning and 12 in the evening. How many liters are left?

**zero_shot** — content=1.00 conformance=0.00 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=x)

```
To find out how many liters are left in the tank, we need to subtract the total amount of liters used from the initial capacity of the tank.

The initial capacity of the tank is 50 liters.

In the morning, 18 liters are used.
In the evening, 12 liters are used.

So, the total amount used during the day is:
\[ 18 \text{ liters} + 12 \text{ liters} = 30 \text{ liters} \]

Subtracting the total amount used from the initial capacity gives us:
\[ 50 \text{ liters} - 30 \text{ liters} = 20 \text{ liters} \]

Therefore, there are 20 liters left in the tank.
```

**full** — content=1.00 conformance=1.00 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Determine the initial amount of water in the tank = 50 liters
Step 2: Subtract the amount used in the morning = 50 - 18 = 32 liters
Step 3: Subtract the amount used in the evening = 32 - 12 = 20 liters
Answer: 20
```

**compressed** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total amount of water used during the day.
18 liters (morning) + 12 liters (evening) = 30 liters

Step 2: Subtract the total amount of water used from the initial amount in the tank.
50 liters (initial) - 30 liters (used) = 20 liters

Answer: 20
```

**style_text** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Determine the total amount of water used during the day.
         Total used = Morning usage + Evening usage
                     = 18 liters + 12 liters
                     = 30 liters
Step 2: Calculate the remaining amount of water in the tank.
         Remaining = Initial amount - Total used
                    = 50 liters - 30 liters
                    = 20 liters
Answer: 20
```

**primed** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total amount of water used during the day.
18 liters (morning) + 12 liters (evening) = 30 liters

Step 2: Subtract the total amount of water used from the initial amount in the tank.
50 liters (initial) - 30 liters (used) = 20 liters

Answer: 20
```

### split_bill

> Three friends split a 60 dollar bill equally. How much does each person pay in dollars?

**zero_shot** — content=1.00 conformance=0.00 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=x)

```
To find out how much each person pays when three friends split a 60 dollar bill equally, you divide the total amount by the number of people.

So, you would calculate:

\[ \text{Amount per person} = \frac{\text{Total amount}}{\text{Number of people}} = \frac{60}{3} = 20 \]

Each person pays 20 dollars.
```

**full** — content=1.00 conformance=0.75 (numbered_steps=x, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: divide total bill by number of friends = 60 / 3 = 20
Answer: 20
```

**compressed** — content=1.00 conformance=0.75 (numbered_steps=x, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Divide the total bill amount by the number of people.
       60 / 3 = 20

Answer: 20
```

**style_text** — content=1.00 conformance=1.00 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Determine the total amount to be split, which is $60.
Step 2: Identify the number of people splitting the bill, which is 3.
Step 3: Divide the total amount by the number of people to find out how much each person pays: 60 / 3 = 20.
Answer: 20
```

**primed** — content=1.00 conformance=0.75 (numbered_steps=x, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Divide the total bill amount by the number of people.
       60 / 3 = 20

Answer: 20
```

### weekly_run

> A runner runs 8 km each day for 5 days. How many km in total?

**zero_shot** — content=0.00 conformance=0.00 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=x)

```
To find the total distance run over 5 days, you multiply the distance run each day by the number of days:

\[ \text{Total Distance} = \text{Distance per Day} \times \text{Number of Days} \]

Given:
- Distance per Day = 8 km
- Number of Days = 5

So,
\[ \text{Total Distance} = 8 \, \text{km/day} \times 5 \, \text{days} = 40 \, \text{km} \]

Therefore, the runner runs a total of 40 kilometers over the 5 days.
```

**full** — content=1.00 conformance=0.75 (numbered_steps=x, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: multiply daily distance by number of days = 8 * 5 = 40
Answer: 40
```

**compressed** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total distance run by multiplying the daily distance by the number of days.
Step 2: 8 km/day * 5 days = 40 km.
Answer: 40.
```

**style_text** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total distance run by multiplying the daily distance by the number of days.
Step 2: 8 km/day * 5 days = 40 km
Answer: 40
```

**primed** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total distance run by multiplying the daily distance by the number of days.
Step 2: 8 km/day * 5 days = 40 km.
Answer: 40.
```

## Domain: writing (full conformance=0.93 -> PASS)

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| zero_shot | 1.00 | 0.07 +/-0.15 | 41 |
| full | 0.93 | 0.93 +/-0.15 | 150 |
| compressed | 1.00 | 0.13 +/-0.18 | 106 |
| style_text | 1.00 | 0.87 +/-0.18 | 152 |
| primed | 1.00 | 0.13 +/-0.18 | 106 |

### gravity

> Explain what gravity is.

**zero_shot** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Gravity is the force of attraction that exists between any two masses, including stars, planets, and even small objects on Earth. It is one of the four fundamental forces in nature and is always attractive, meaning it pulls objects together rather than pushing them apart. On Earth, gravity gives weight to physical objects and causes things to fall towards the ground when dropped. The strength of gravitational force depends on the masses of the objects and the distance between them, as described by Newton's law of universal gravitation. This force keeps our feet firmly planted on the ground and also governs the motion of celestial bodies in space, such as the orbits of planets around the sun.
```

**full** — content=1.00 conformance=1.00 (second_person=PASS, no_contractions=PASS, bulleted_list=PASS)

```
- You can understand gravity as the force that pulls objects towards each other.
- It is the reason why you stay on the ground and do not float away into space.
- Gravity is stronger between objects that have more mass and closer together.
```

**compressed** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Gravity is the natural phenomenon by which all physical bodies attract each other, including planets, stars, and galaxies. This attraction is due to the mass of these objects and is described by Newton's law of universal gravitation, which states that every particle attracts every other particle in the universe with a force that is directly proportional to the product of their masses and inversely proportional to the square of the distance between their centers. Gravity is the force that keeps objects on the Earth's surface and governs the motion of celestial bodies in space.
```

**style_text** — content=1.00 conformance=0.67 (second_person=PASS, no_contractions=x, bulleted_list=PASS)

```
- You should understand gravity as the force that attracts a body toward another body, most commonly described as the force that pulls objects towards the center of the Earth.
- You will recognize that gravity is what gives weight to objects and causes them to fall to the ground when dropped.
- You may note that gravity is one of the four fundamental forces of nature, and it acts between all objects that have mass.
- You can observe its effects in everyday life, such as when you see an apple falling from a tree or feel your feet firmly on the ground.
- You should be aware that the strength of gravitational attraction depends on the masses of the objects and the distance between them, as described by Newton's law of universal gravitation.
```

**primed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Gravity is the natural phenomenon by which physical bodies attract each other with a force proportional to their masses and the distance between them. It is one of the fundamental forces of nature, responsible for keeping objects on the Earth’s surface, causing tides, and influencing the orbits of planets around the sun. The strength of gravitational attraction depends on the mass of the objects and decreases with the square of the distance between their centers. This force was described mathematically by Sir Isaac Newton in his law of universal gravitation.
```

### vaccine

> Explain what a vaccine does.

**zero_shot** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
A vaccine is a biological preparation that helps the body's immune system recognize and fight off specific diseases caused by pathogens like viruses or bacteria. It typically contains components similar to or derived from the disease-causing organism, but these components are weakened, inactivated, or only parts of the pathogen (like proteins). When introduced into the body, the immune system recognizes these components as foreign and mounts an immune response, producing antibodies and memory cells. This prepares the body to respond more effectively and rapidly if it encounters the actual pathogen in the future, preventing illness or reducing its severity.
```

**full** — content=0.67 conformance=1.00 (second_person=PASS, no_contractions=PASS, bulleted_list=PASS)

```
- You should understand that a vaccine works by training your immune system to recognize and fight off specific diseases.
- It introduces a small, harmless piece of the virus or bacteria, known as an antigen, which prompts your body to produce a defensive response.
- You will develop immunity to the disease without having to suffer through the illness itself, allowing your body to remember how to fight it off quickly if you encounter the real pathogen in the future.
```

**compressed** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
A vaccine is a biological preparation designed to enhance the immune system's ability to fight off specific diseases. It typically contains components derived from weakened or inactivated forms of the disease-causing pathogen, such as viruses or bacteria. When introduced into the body, the immune system recognizes these components as foreign and mounts an immune response, producing antibodies and memory cells. This prepares the body to respond more effectively and rapidly if it encounters the actual pathogen in the future, thereby preventing the development of the disease or reducing its severity.
```

**style_text** — content=1.00 conformance=1.00 (second_person=PASS, no_contractions=PASS, bulleted_list=PASS)

```
- You should understand that a vaccine is designed to prepare your immune system to recognize and combat specific diseases.
- You will receive a vaccine that contains components resembling disease-causing pathogens, but these components are either weakened or inactivated so they do not cause the disease itself.
- You may experience an immune response after vaccination, which involves the production of antibodies and memory cells that can quickly respond if you encounter the actual pathogen in the future.
- You should be aware that vaccines play a crucial role in preventing infectious diseases and contribute to the overall health of populations through herd immunity.
```

**primed** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
A vaccine is designed to help the body's immune system recognize and fight off specific pathogens, such as viruses or bacteria, without causing the disease itself. It typically contains weakened, inactivated, or parts of the pathogen, which triggers an immune response. This response leads to the production of antibodies and the creation of memory cells within the immune system. If the vaccinated individual later encounters the actual pathogen, their immune system can quickly recognize it and mount a rapid and effective defense, preventing the development of the disease or reducing its severity.
```

### tides

> Explain what causes ocean tides.

**zero_shot** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Ocean tides are primarily caused by the gravitational pull of the Moon and the Sun on Earth's oceans. The Moon, being closer to Earth, has the most significant influence. As the Earth rotates, different parts of the planet face the Moon, causing the water in the oceans to bulge out towards the Moon due to its gravitational pull. This creates one high tide. On the opposite side of the Earth, another high tide occurs because the Earth itself is also being pulled slightly away from the water on that side. Low tides occur in the regions where the ocean water is neither being pulled towards the Moon nor away from it. The Sun also exerts a gravitational force on the Earth's oceans, though its effect is less than that of the Moon because it is much farther away. When the Sun, Moon, and Earth align (during full or new moons), their combined gravitational forces create higher than normal tides known as spring tides. Conversely, when the Sun and Moon are at right angles relative to Earth, their gravitational forces partially cancel each other out, leading to lower than normal tides called neap tides.
```

**full** — content=1.00 conformance=0.67 (second_person=PASS, no_contractions=x, bulleted_list=PASS)

```
- You should understand that ocean tides are primarily caused by the gravitational pull between the Earth and the Moon.
- You may observe that the Moon's gravity pulls on the Earth's oceans, creating a bulge of water on the side of the Earth facing the Moon.
- You will also note that another bulge occurs on the opposite side of the Earth due to the centrifugal force of the Earth-Moon system orbiting their common center of mass.
- You might recognize that as the Earth rotates, different parts of the planet face the Moon, experiencing high tides, while other parts experience low tides.
```

**compressed** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Ocean tides are caused primarily by the gravitational pull of the Moon and, to a lesser extent, the Sun on Earth's oceans. As the Earth rotates on its axis, different parts of the planet face the Moon and Sun at different times, leading to variations in their gravitational effects. The Moon, being closer to Earth, has a more significant impact on tides. Its gravity pulls water in the oceans toward itself, creating a bulge of water on the side of Earth facing the Moon. A similar bulge occurs on the opposite side of Earth due to the differential gravitational forces across Earth's diameter. As Earth rotates, these bulges move around the planet, causing areas to experience high tides (when they're under a bulge) and low tides (when they're not). The Sun also exerts gravitational force on Earth's oceans, but because it is much farther away, its effect is less pronounced. When the Sun, Earth, and Moon align, during full or new moons, their combined gravitational forces create spring tides, which have higher high tides and lower low tides than average. Conversely, when the Sun and Moon are at right angles relative to Earth, neap tides occur, resulting in less extreme tidal changes.
```

**style_text** — content=1.00 conformance=0.67 (second_person=PASS, no_contractions=x, bulleted_list=PASS)

```
- You should understand that ocean tides are primarily caused by the gravitational pull exerted by the Moon and the Sun on Earth.
- You will find that the Moon plays a more significant role due to its closer proximity to Earth, despite the Sun's greater mass.
- You may note that as the Earth rotates, different parts of the planet face the Moon and the Sun, leading to high tides when these celestial bodies pull the water outward.
- You should also be aware that low tides occur in areas not directly aligned with the Moon or the Sun, as the gravitational pull is less strong there.
- You might observe that the interaction between the gravitational forces of the Moon and the Sun can lead to spring tides (when they align) and neap tides (when they are at right angles to each other), affecting the height of the tides.
```

**primed** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Ocean tides are caused primarily by the gravitational pull of the Moon and, to a lesser extent, the Sun on Earth's oceans. As the Earth rotates on its axis, different parts of the planet face the Moon and Sun at different times, leading to variations in their gravitational effects. The Moon, being closer to Earth, has a more significant impact on tides. Its gravity pulls water in the oceans towards it, causing a bulge on the side of Earth facing the Moon. A similar bulge occurs on the opposite side of Earth due to the differential gravitational forces across Earth's diameter. As Earth rotates, these bulges move around the planet, creating the rising (flood tide) and falling (ebb tide) of sea levels we observe as tides. The Sun also influences tides, but its effect is less pronounced because it is much farther away from Earth than the Moon. When the Sun, Earth, and Moon align, during full or new moons, their combined gravitational forces create higher high tides and lower low tides, known as spring tides. Conversely, when the Sun and Moon are at right angles relative to Earth, their gravitational forces partially cancel each other out, resulting in neap tides, which have less extreme tidal ranges.
```

### friction

> Explain what friction is.

**zero_shot** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Friction is a force that resists the relative motion of surfaces sliding against each other. It occurs when two surfaces come into contact and try to move past one another, creating resistance due to the interactions at the microscopic level where tiny bumps and imperfections on the surfaces interact. This force can convert kinetic energy into thermal energy (heat) and is essential for many everyday activities, such as walking or braking in vehicles, but it can also cause wear and tear on materials over time.
```

**full** — content=1.00 conformance=1.00 (second_person=PASS, no_contractions=PASS, bulleted_list=PASS)

```
- You should understand that friction is a force that resists the motion of objects moving against each other.
- It occurs when two surfaces come into contact and try to move past one another.
- You will find that the rougher the surfaces, the more friction there is between them.
- This force acts in the direction opposite to the motion or attempted motion of the object.
```

**compressed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Friction is the force that resists the relative motion of surfaces sliding against each other. It occurs due to the interactions between the molecules or roughness on the surfaces in contact. The amount of friction depends on the types of materials and the normal force pressing them together. Friction can be beneficial, like enabling us to walk without slipping, or detrimental, such as causing wear and tear on machinery parts.
```

**style_text** — content=1.00 conformance=1.00 (second_person=PASS, no_contractions=PASS, bulleted_list=PASS)

```
- You should understand friction as the resistance that one surface or object encounters when moving over another.
- You will find that friction acts to oppose motion between the two surfaces in contact.
- You may observe that the amount of friction depends on the types of materials in contact and the force pressing them together.
```

**primed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Friction is the force that resists the relative motion of surfaces sliding against each other. It occurs due to the interactions between the molecules or roughness on the surfaces in contact. The amount of friction depends on the types of materials and the normal force pressing them together. Friction can be beneficial, like enabling us to walk without slipping, or detrimental, such as causing wear and reducing efficiency in machinery.
```

### evaporation

> Explain what evaporation is.

**zero_shot** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Evaporation is the process by which water changes from its liquid state to a gaseous state (water vapor) at temperatures below its boiling point. This process occurs at the surface of a liquid and is influenced by factors such as temperature, humidity, wind speed, and the surface area of the liquid. Evaporation plays a crucial role in the water cycle, helping to regulate the Earth's climate and providing moisture for precipitation.
```

**full** — content=1.00 conformance=1.00 (second_person=PASS, no_contractions=PASS, bulleted_list=PASS)

```
- You can understand evaporation as the process where water transforms from its liquid state into vapor.
- It occurs when water molecules at the surface gain sufficient energy to break free from the liquid and enter the air as water vapor.
- You may observe that this process accelerates with an increase in temperature or when there is more wind.
```

**compressed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Evaporation is the process by which a liquid transforms into a gas at temperatures below its boiling point. It occurs when individual molecules at the surface of a liquid gain enough kinetic energy to overcome the intermolecular forces holding them in the liquid state, thus escaping into the air as vapor. The rate of evaporation increases with temperature, as higher temperatures provide more energy to the molecules, making it easier for them to break free from the liquid and enter the gaseous state.
```

**style_text** — content=1.00 conformance=1.00 (second_person=PASS, no_contractions=PASS, bulleted_list=PASS)

```
- You should understand that evaporation is the process by which water changes from a liquid state to a gaseous state, known as water vapor.
- You will find that this process happens at the surface of a liquid and does not require the liquid to reach its boiling point.
- You may notice that the rate of evaporation can be influenced by factors such as temperature, humidity, and wind speed, with higher temperatures generally leading to faster rates of evaporation.
```

**primed** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Evaporation is the process by which a liquid transforms into a gas at temperatures below its boiling point. This occurs as individual molecules on the liquid's surface gain enough kinetic energy to overcome the intermolecular forces holding them in the liquid state, thus escaping into the air as vapor. The rate of evaporation generally increases with temperature, as higher temperatures provide more energy for molecules to break free from the liquid.
```
