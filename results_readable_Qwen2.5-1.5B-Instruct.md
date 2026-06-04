# Primer harness run (Qwen/Qwen2.5-1.5B-Instruct, split=test, seeds=[0], regime=compressed)

## Overall

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| zero_shot | 0.87 | 0.26 +/-0.27 | 53 |
| full | 0.91 | 0.63 +/-0.27 | 203 |
| compressed | 0.87 | 0.47 +/-0.29 | 112 |
| style_text | 0.87 | 0.66 +/-0.30 | 156 |
| primed | 0.93 | 0.47 +/-0.29 | 112 |

## Value (cost-adjusted: primer vs re-pasted text rival)

| scope | conf gain vs compressed | conf vs style_text | tokens vs style_text | verdict |
|---|---|---|---|---|
| coding | +0.00 | -0.20 | -43 | mixed (trade-off) |
| math (below gate) | +0.00 | -0.25 | -43 | mixed (trade-off) |
| writing (below gate) | +0.00 | -0.13 | -46 | mixed (trade-off) |
| **gated overall** | +0.00 | -0.20 | -43 | mixed (trade-off) |

## Domain: coding (full conformance=0.80 -> PASS)

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| zero_shot | 0.80 | 0.55 +/-0.21 | 61 |
| full | 0.80 | 0.80 +/-0.11 | 235 |
| compressed | 0.80 | 0.70 +/-0.27 | 107 |
| style_text | 0.60 | 0.90 +/-0.14 | 150 |
| primed | 0.80 | 0.70 +/-0.27 | 107 |

### dedupe_preserve_order

> Write a function `dedupe(items: list) -> list` that removes duplicates while preserving first-seen order.

**zero_shot** — content=0.00 conformance=0.50 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=x)

```
```python
from typing import List

def dedupe(items: List) -> List:
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)

# Example usage:
if __name__ == "__main__":
    sample_list = [1, 2, 2, 3, 4, 4, 5]
    unique_items = list(dedupe(sample_list))
    print(unique_items)
```

This Python code defines a function `dedupe` that takes a list of items and returns a new list with duplicates removed, maintaining the original order of the first occurrence of each element. The `seen` set is used to keep track of elements that have already been encountered. For each item in the input list, it checks whether the item has been seen before using the `not in` operator on the `seen` set. If the item hasn't been seen (i.e., it's the first time we've seen it), it yields the item and adds it to the `seen` set so that future occurrences of this item will also be yielded without being added again.
```

**full** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
from typing import List

def dedupe(items: List) -> List:
    """
    Return a new list without any duplicate items from the original list.
    
    >>> dedupe([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> dedupe(['apple', 'banana', 'apple', 'pear'])
    ['apple', 'banana', 'pear']
    >>> dedupe([])
    []
    """
    seen = set()
    deduped_list = []
    for item in items:
        if item not in seen:
            seen.add(item)
            deduped_list.append(item)
    return deduped_list
```
```

**compressed** — content=1.00 conformance=0.25 (snake_case=PASS, type_hints=x, raises_valueerror=x, docstring=x)

```
```python
def dedupe(items):
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]
```

This function uses a set to keep track of seen elements and filters out any duplicates as it iterates through the input list. The use of `seen.add(x)` ensures that each element is added to the set exactly once, maintaining the order of first occurrence.
```

**style_text** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
from typing import List

def dedupe(items: List) -> List:
    """
    Remove duplicates from a list while preserving the order of items.
    
    Args:
        items (List): A list of hashable elements.
        
    Returns:
        List: A new list with duplicates removed, maintaining original order.
    """
    seen = set()
    deduped_list = []
    for item in items:
        if item not in seen:
            seen.add(item)
            deduped_list.append(item)
    return deduped_list
```
```

**primed** — content=1.00 conformance=0.25 (snake_case=PASS, type_hints=x, raises_valueerror=x, docstring=x)

```
```python
def dedupe(items):
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]
```

This function uses a set to keep track of seen elements and filters out any duplicates as it iterates through the input list. The use of `seen.add(x)` ensures that each element is added to the set exactly once, maintaining the order of first occurrence.
```

### word_frequencies

> Write a function `word_freq(text: str) -> dict` mapping each lowercased word to its count.

**zero_shot** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
from typing import Dict

def word_freq(text: str) -> Dict[str, int]:
    """
    Maps each unique lowercased word in the given text to its frequency.
    
    Parameters:
    - text (str): The input string containing words separated by spaces.
    
    Returns:
    - Dict[str, int]: A dictionary where keys are unique lowercased words and values are their respective counts.
    """
    # Convert the text to lowercase and split into words
    words = text.lower().split()
    
    # Use a dictionary comprehension to map each word to its count
    return {word: words.count(word) for word in set(words)}

# Example usage
if __name__ == "__main__":
    example_text = "Hello world hello Python programming"
    print(word_freq(example_text))
```

This code snippet defines a function `word_freq` that takes a string as input and returns a dictionary with the frequency of each unique lowercased word found in the input text. It uses a dictionary comprehension to efficiently calculate these frequencies.
```

**full** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
from typing import Dict, List

def word_freq(text: str) -> Dict[str, int]:
    """
    Return a dictionary mapping each unique lowercased word in the given text to its frequency.
    
    Args:
    - text (str): The input text from which to calculate word frequencies.
    
    Returns:
    - Dict[str, int]: A dictionary where keys are words and values are their respective counts.
    """
    # Normalize the text to lowercase and split into words
    words = text.lower().split()
    
    # Use a Counter to count occurrences of each word
    word_counts = {word: words.count(word) for word in set(words)}
    
    return word_counts
```
```

**compressed** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
from typing import Dict

def word_freq(text: str) -> Dict[str, int]:
    """
    Returns a dictionary of words from the input text, where keys are lowercase words and values are their counts.
    
    >>> word_freq("Hello world! Hello everyone.")
    {'hello': 2, 'world': 1, 'everyone': 1}
    """
    return {word.lower(): text.count(word) for word in set(text.split())}
```
```

**style_text** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
from typing import Dict, List

def word_freq(text: str) -> Dict[str, int]:
    """
    Returns a dictionary of words from the given text, where keys are lowercase words and values are their counts.
    
    :param text: A string containing the text to analyze.
    :return: A dictionary mapping each unique lowercased word to its frequency in the text.
    """
    # Normalize the text to lowercase and split into words
    words = text.lower().split()
    
    # Use a Counter to count occurrences of each word
    word_counts = {word: words.count(word) for word in set(words)}
    
    return word_counts
```
```

**primed** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
def word_freq(text: str) -> dict:
    """
    Returns a dictionary of words from the input text, where keys are lowercase words and values are their counts.
    
    >>> word_freq("Hello world! Hello everyone.")
    {'hello': 2, 'world': 1, 'everyone': 1}
    """
    return {word.lower(): text.count(word) for word in set(text.split())}
```
```

### running_max

> Write a function `running_max(nums: list) -> list` returning the cumulative maximum at each index.

**zero_shot** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
from typing import List

def running_max(nums: List[int]) -> List[int]:
    """
    Returns a new list where each element is the maximum value encountered up to that point.
    
    :param nums: List of integers
    :return: A list containing the cumulative maximum values
    """
    if not nums:
        return []
    
    max_values = [nums[0]]
    for num in nums[1:]:
        max_values.append(max(num, max_values[-1]))
    
    return max_values
```

This Python function `running_max` takes a list of integers as input and returns a new list where each element is the maximum value encountered so far from the start of the original list. It iterates through the input list once, maintaining a running maximum using an auxiliary list `max_values`. The final result is constructed by appending these maximums to the end of the input list.
```

**full** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
from typing import List

def running_max(nums: List[int]) -> List[int]:
    """
    Return a new list where each element is the cumulative maximum up to that point.
    
    >>> running_max([1, 2, 3, 2, 3])
    [1, 2, 3, 3, 3]
    >>> running_max([-1, -2, -3, -4, -5])
    [-1, -1, -1, -1, -1]
    """

    if not nums:
        return []

    result = []
    current_max = nums[0]

    for num in nums:
        if num > current_max:
            current_max = num
        result.append(current_max)

    return result
```
```

**compressed** — content=0.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def running_max(nums: list) -> list:
    """
    Returns a new list where each element is the cumulative maximum up to that point.
    
    Args:
        nums (list): A list of integers or floats.
        
    Returns:
        list: A list containing the cumulative maximum values.
    """
    if not nums:
        raise ValueError("Input list cannot be empty.")
    
    max_values = [nums[0]]
    for num in nums[1:]:
        if num > max_values[-1]:
            max_values.append(num)
        else:
            max_values[-1] = num
    
    return max_values
```
```

**style_text** — content=0.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
from typing import List

def running_max(nums: List[int]) -> List[int]:
    """
    Returns a new list where each element is the cumulative maximum up to that point.
    
    Args:
        nums (List[int]): A list of integers.
        
    Returns:
        List[int]: A list containing the cumulative maximum values.
    """
    if not nums:
        raise ValueError("Input list cannot be empty")
    
    max_ending_here = max_so_far = nums[0]
    result = [max_ending_here]
    
    for num in nums[1:]:
        max_ending_here = max(num, max_ending_here)
        max_so_far = max(max_so_far, max_ending_here)
        result.append(max_so_far)
    
    return result
```
```

**primed** — content=0.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
def running_max(nums: list) -> list:
    """
    Calculate the cumulative maximum of a given list of numbers.
    
    Args:
        nums (list): A list of numeric values.
        
    Returns:
        list: A list containing the cumulative maximum value at each index.
    """
    if not nums:
        raise ValueError("Input list cannot be empty.")
    
    max_values = [nums[0]]
    for num in nums[1:]:
        if num > max_values[-1]:
            max_values.append(num)
        else:
            max_values[-1] = num
    
    return max_values

# Example usage:
print(running_max([1, 2, 3, 2, 3, 4]))  # Output: [1, 2, 3, 3, 3, 4]
```
```

### average

> Write a function `average(nums: list) -> float` returning the arithmetic mean of the numbers.

**zero_shot** — content=1.00 conformance=0.25 (snake_case=PASS, type_hints=x, raises_valueerror=x, docstring=x)

```
```python
def average(nums):
    return sum(nums) / len(nums)
```
```

**full** — content=0.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
from typing import List

def average(nums: List[float]) -> float:
    """
    Return the arithmetic mean of the given list of numbers.
    
    Args:
    nums (List[float]): A list of floating-point numbers.
    
    Returns:
    float: The arithmetic mean of the numbers.
    
    Raises:
    ValueError: If 'nums' is not a list or contains non-float elements.
    """

    if not isinstance(nums, list):
        raise ValueError("nums must be a list")
    
    if any(not isinstance(num, float) for num in nums):
        raise ValueError("All elements in nums must be floats")
    
    return sum(nums) / len(nums)
```
```

**compressed** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=x)

```
```python
def average(nums: list) -> float:
    if not nums:
        raise ValueError("Input list is empty")
    
    return sum(nums) / len(nums)
```
```

**style_text** — content=0.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
from typing import List, Float

def average(nums: List[float]) -> Float:
    """
    Calculate the arithmetic mean of a list of numbers.
    
    Args:
        nums (List[float]): A list of floating-point numbers.
        
    Returns:
        Float: The arithmetic mean of the numbers.
        
    Raises:
        ValueError: If 'nums' is not a list or contains non-float elements.
    """
    if not isinstance(nums, list):
        raise ValueError("Input must be a list.")
    if any(not isinstance(num, float) for num in nums):
        raise ValueError("All elements in the list must be floats.")
    
    return sum(nums) / len(nums)
```
```

**primed** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=x)

```
```python
def average(nums: list) -> float:
    if not nums:
        raise ValueError("Input list is empty")
    
    return sum(nums) / len(nums)
```
```

### flatten

> Write a function `flatten(matrix: list) -> list` that concatenates a list of lists into one flat list.

**zero_shot** — content=1.00 conformance=0.50 (snake_case=PASS, type_hints=x, raises_valueerror=x, docstring=PASS)

```
```python
def flatten(matrix):
    """
    Concatenates a list of lists into one flat list.
    
    Parameters:
    matrix (list): A list of lists to be flattened.
    
    Returns:
    list: A single list containing all elements from the input lists.
    """
    return [item for sublist in matrix for item in sublist]

# Example usage:
matrix = [[1, 2, 3], [4, 5], [6]]
print(flatten(matrix))  # Output: [1, 2, 3, 4, 5, 6]
```
```

**full** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
from typing import List

def flatten(matrix: List[List[int]]) -> List[int]:
    """
    Flatten a matrix represented as a list of lists into a single list.
    
    Args:
    - matrix: A list of lists where each sublist represents a row in the matrix.
    
    Returns:
    - A flattened list containing all elements from the matrix.
    """
    return [item for sublist in matrix for item in sublist]
```
```

**compressed** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
def flatten(matrix: list) -> list:
    """
    Concatenates a list of lists into one flat list.
    
    Args:
        matrix (list): A list of lists to be flattened.
        
    Returns:
        list: A single list containing all elements from the input lists.
        
    Raises:
        ValueError: If any element within the input is not a list or if the input itself is not a list.
    """
    return [item for sublist in matrix for item in sublist]
```
```

**style_text** — content=1.00 conformance=1.00 (snake_case=PASS, type_hints=PASS, raises_valueerror=PASS, docstring=PASS)

```
```python
from typing import List

def flatten(matrix: List[List[int]]) -> List[int]:
    """
    Flattens a given matrix (list of lists) into a single list.
    
    Args:
        matrix (List[List[int]]): A 2D list representing the matrix to be flattened.
        
    Returns:
        List[int]: A single list containing all elements from the original matrix.
        
    Raises:
        ValueError: If the input is not a valid 2D list.
    """
    if not isinstance(matrix, list) or any(not isinstance(row, list) for row in matrix):
        raise ValueError("Input must be a non-empty 2D list.")
    
    return [item for sublist in matrix for item in sublist]
```
```

**primed** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
def flatten(matrix: list) -> list:
    """
    Concatenates a list of lists into one flat list.
    
    Args:
        matrix (list): A list of lists to be flattened.
        
    Returns:
        list: A single list containing all elements from the input lists.
        
    Raises:
        ValueError: If any element within the input is not a list.
    """
    return [item for sublist in matrix for item in sublist]
```
```

## Domain: math (full conformance=0.75 -> BELOW GATE (capability-bound))

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| zero_shot | 0.80 | 0.10 +/-0.14 | 57 |
| full | 1.00 | 0.75 +/-0.18 | 223 |
| compressed | 0.80 | 0.50 +/-0.18 | 151 |
| style_text | 1.00 | 0.75 +/-0.18 | 194 |
| primed | 1.00 | 0.50 +/-0.18 | 151 |

### pages_left

> A book has 120 pages. Ada read 45 pages on Monday and 35 on Tuesday. How many pages are left?

**zero_shot** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=PASS, answer_line=x, no_prose_intro=x)

```
Ada started with 120 pages in the book.

On Monday, she read 45 pages.
On Tuesday, she read an additional 35 pages.

To find out how many pages she has left to read, we subtract the total number of pages she has already read from the original number of pages:

Total pages read = Pages read on Monday + Pages read on Tuesday
Total pages read = 45 + 35

Now let's calculate that:
Total pages read = 80

Pages left to read = Original number of pages - Total pages read
Pages left to read = 120 - 80

Let's do the subtraction:
Pages left to read = 40

So, Ada has 40 pages left to read.
```

**full** — content=1.00 conformance=1.00 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Subtract the number of pages read on Monday from the total number of pages.
   Step 1a: 120 - 45 = 75
   Answer: 75

Step 2: Subtract the number of pages read on Tuesday from the remaining pages after Monday.
   Step 2a: 75 - 35 = 40
   Answer: 40

Final answer: There are 40 pages left.
```

**compressed** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=x, no_prose_intro=PASS)

```
Step 1: Calculate the total number of pages Ada read over the two days.
Ada read 45 pages on Monday and 35 pages on Tuesday.
Total pages read = 45 + 35 = 80 pages

Step 2: Subtract the total number of pages read from the original number of pages in the book to find out how many pages are left.
Original number of pages = 120
Pages left = Original number of pages - Total pages read
Pages left = 120 - 80 = 40 pages

Answer: There are 40 pages left in the book.
```

**style_text** — content=1.00 conformance=1.00 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total number of pages Ada read from Monday to Tuesday.
   - Pages read on Monday: 45
   - Pages read on Tuesday: 35
   
   Total pages read = 45 + 35

Step 2: Perform the addition to find out how many pages Ada read in total.
   Total pages read = 80

Step 3: Subtract the total number of pages read from the original number of pages in the book.
   Original number of pages: 120
   Pages left = 120 - 80

Step 4: Perform the subtraction to find out how many pages are left.
   Pages left = 40

Answer: 40 pages.
```

**primed** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=x, no_prose_intro=PASS)

```
Step 1: Calculate the total number of pages Ada read over the two days.
Ada read 45 pages on Monday and 35 pages on Tuesday.
Total pages read = 45 + 35

Step 2: Perform the addition to find the total number of pages read.
Total pages read = 80

Step 3: Subtract the total number of pages read from the original number of pages in the book.
Pages left = Total pages in the book - Total pages read
Pages left = 120 - 80

Step 4: Perform the subtraction to find the remaining number of pages.
Pages left = 40

Answer: There are 40 pages left in the book.
```

### hen_eggs

> A farmer has 5 hens and each lays 6 eggs. How many eggs in total?

**zero_shot** — content=1.00 conformance=0.00 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=x)

```
To determine the total number of eggs laid by the farmer's hens, we can follow these steps:

1. Identify the number of hens: The farmer has 5 hens.
2. Determine how many eggs each hen lays: Each hen lays 6 eggs.
3. Calculate the total number of eggs by multiplying the number of hens by the number of eggs each hen lays.

The calculation is as follows:
\[ \text{Total number of eggs} = \text{Number of hens} \times \text{Eggs per hen} \]
\[ \text{Total number of eggs} = 5 \times 6 \]
\[ \text{Total number of eggs} = 30 \]

So, the total number of eggs laid by the farmer's hens is **30**.
```

**full** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Multiply the number of hens by the number of eggs each hen lays.
   Step 2: Calculate the total number of eggs.

Answer: 30
```

**compressed** — content=1.00 conformance=0.50 (numbered_steps=x, shows_arithmetic=PASS, answer_line=x, no_prose_intro=PASS)

```
Step 1: Calculate the total number of eggs laid by all the hens.
Each hen lays 6 eggs, and there are 5 hens.
So, 5 * 6 = 30 eggs in total.

Answer: The farmer has 30 eggs in total.
```

**style_text** — content=1.00 conformance=0.75 (numbered_steps=x, shows_arithmetic=PASS, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the number of eggs laid by all the hens together.
   Each hen lays 6 eggs, and there are 5 hens.
   So, we multiply the number of hens by the number of eggs each hen lays:
   5 * 6 = 30 eggs.

Answer: 30 eggs.
```

**primed** — content=1.00 conformance=0.50 (numbered_steps=x, shows_arithmetic=PASS, answer_line=x, no_prose_intro=PASS)

```
Step 1: Calculate the total number of eggs laid by all the hens.
   Each hen lays 6 eggs, and there are 5 hens.
   So, 5 * 6 = 30 eggs.

Answer: The farmer has a total of 30 eggs.
```

### tank_left

> A tank holds 50 liters. 18 liters are used in the morning and 12 in the evening. How many liters are left?

**zero_shot** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=PASS, answer_line=x, no_prose_intro=x)

```
To determine how many liters of water are left in the tank after using some in the morning and others in the evening, we can follow these steps:

1. Start with the total amount of water in the tank.
   \[
   \text{Total water} = 50 \text{ liters}
   \]

2. Subtract the amount of water used in the morning from the total amount.
   \[
   \text{Water remaining after morning} = 50 - 18 = 32 \text{ liters}
   \]

3. Subtract the amount of water used in the evening from the remaining amount.
   \[
   \text{Water remaining after evening} = 32 - 12 = 20 \text{ liters}
   \]

So, the number of liters of water left in the tank is:
\[
\boxed{20}
\]
```

**full** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Subtract the amount used in the morning from the total capacity.
   Step 1a: 50 liters - 18 liters = 32 liters remaining.

Step 2: Subtract the amount used in the evening from the remaining amount.
   Step 2a: 32 liters - 12 liters = 20 liters remaining.

Answer: 20 liters are left.
```

**compressed** — content=1.00 conformance=0.50 (numbered_steps=PASS, shows_arithmetic=x, answer_line=x, no_prose_intro=PASS)

```
Step 1: Start with the total amount of water in the tank.
Total water = 50 liters

Step 2: Subtract the amount used in the morning.
Water remaining after morning use = Total water - Morning usage
Water remaining after morning use = 50 liters - 18 liters
Water remaining after morning use = 32 liters

Step 3: Subtract the amount used in the evening.
Water remaining after evening use = Water remaining after morning use - Evening usage
Water remaining after evening use = 32 liters - 12 liters
Water remaining after evening use = 20 liters

Answer: There are 20 liters of water left in the tank.
```

**style_text** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the total amount of water used in the day.
   Total used = Morning usage + Evening usage
              = 18 liters + 12 liters
              = 30 liters

Step 2: Subtract the total used from the initial capacity to find out how much is left.
   Remaining = Initial capacity - Total used
             = 50 liters - 30 liters
             = 20 liters

Answer: 20 liters.
```

**primed** — content=1.00 conformance=0.50 (numbered_steps=PASS, shows_arithmetic=x, answer_line=x, no_prose_intro=PASS)

```
Step 1: Start with the total amount of water in the tank.
Total water = 50 liters

Step 2: Subtract the amount used in the morning.
Water remaining after morning use = Total water - Morning usage
Water remaining after morning use = 50 liters - 18 liters
Water remaining after morning use = 32 liters

Step 3: Subtract the amount used in the evening.
Water remaining after evening use = Water remaining after morning use - Evening usage
Water remaining after evening use = 32 liters - 12 liters
Water remaining after evening use = 20 liters

Answer: There are 20 liters of water left in the tank.
```

### split_bill

> Three friends split a 60 dollar bill equally. How much does each person pay in dollars?

**zero_shot** — content=1.00 conformance=0.00 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=x)

```
To determine how much each friend pays when splitting a $60 bill equally among three friends, you would divide the total amount by the number of people:

\[ \text{Amount per person} = \frac{\$60}{3} \]

\[ \text{Amount per person} = \$20 \]

So, each person pays $20.
```

**full** — content=1.00 conformance=0.50 (numbered_steps=x, shows_arithmetic=PASS, answer_line=x, no_prose_intro=PASS)

```
Step 1: Divide total amount by number of people = 60 / 3 = 20
Answer: Each person pays $20.
```

**compressed** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=PASS)

```
Step 1: Divide the total amount by the number of people to find out how much each person pays.
Answer: Each person pays $20.
```

**style_text** — content=1.00 conformance=0.50 (numbered_steps=x, shows_arithmetic=PASS, answer_line=x, no_prose_intro=PASS)

```
Step 1: Divide the total amount by the number of people to find out how much each person pays. 
   60 / 3 = 20

Answer: Each person pays $20.
```

**primed** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=PASS)

```
Step 1: Divide the total amount by the number of people to find out how much each person pays.
Answer: Each person pays $20.
```

### weekly_run

> A runner runs 8 km each day for 5 days. How many km in total?

**zero_shot** — content=0.00 conformance=0.00 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=x)

```
To calculate the total distance run by the runner over 5 days, you simply multiply the daily distance by the number of days:

Total Distance = Daily Distance × Number of Days

Plugging in the values given:

Total Distance = 8 km/day × 5 days

Total Distance = 40 km

So, the runner will have covered a total of 40 kilometers over the 5 days.
```

**full** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Multiply the distance run each day by the number of days.
   Step 2: Calculate the total distance.

Answer: 40 km
```

**compressed** — content=0.00 conformance=0.50 (numbered_steps=PASS, shows_arithmetic=x, answer_line=x, no_prose_intro=PASS)

```
Step 1: Calculate the distance run per day.
Distance per day = Distance per row * Number of rows
Distance per day = 8 km * 4
Distance per day = 32 km

Step 2: Calculate the total distance run over 5 days.
Total distance = Distance per day * Number of days
Total distance = 32 km * 5
Total distance = 160 km

Answer: The runner ran a total of 160 kilometers.
```

**style_text** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=x, answer_line=PASS, no_prose_intro=PASS)

```
Step 1: Calculate the distance run per day.
   Distance per day = 8 km

Step 2: Multiply the daily distance by the number of days to find the total distance.
   Total distance = 8 km/day × 5 days

Step 3: Perform the multiplication.
   Total distance = 40 km

Answer: 40 km.
```

**primed** — content=1.00 conformance=0.50 (numbered_steps=PASS, shows_arithmetic=x, answer_line=x, no_prose_intro=PASS)

```
Step 1: Calculate the distance run per day.
Distance per day = 8 km

Step 2: Multiply the daily distance by the number of days.
Total distance = Distance per day × Number of days
Total distance = 8 km/day × 5 days
Total distance = 40 km

Answer: The runner ran a total of 40 kilometers.
```

## Domain: writing (full conformance=0.33 -> BELOW GATE (capability-bound))

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| zero_shot | 1.00 | 0.13 +/-0.18 | 41 |
| full | 0.93 | 0.33 +/-0.24 | 150 |
| compressed | 1.00 | 0.20 +/-0.18 | 78 |
| style_text | 1.00 | 0.33 +/-0.24 | 124 |
| primed | 1.00 | 0.20 +/-0.18 | 78 |

### gravity

> Explain what gravity is.

**zero_shot** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Gravity is the force that attracts two bodies with mass towards each other. It is an attractive force and acts between any two objects that have mass. The strength of the gravitational force depends on the masses of the objects and their distance apart. For example, the Earth's gravity pulls objects toward its center, causing them to fall down when dropped or thrown. This force also causes planets to orbit around stars and keeps satellites in orbit around Earth. Gravity plays a crucial role in shaping the universe and determining the behavior of celestial bodies.
```

**full** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Gravity is the force that attracts objects with mass towards each other. - It causes things to fall down and keeps planets orbiting around stars. - The strength of gravity decreases with distance from the center of mass.
```

**compressed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Gravity is a fundamental force of nature that attracts all objects with mass towards each other. It causes planets to orbit stars and gives weight to objects on Earth. The strength of gravity decreases with distance from the source of gravity (like the center of the Earth).
```

**style_text** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Gravity: The force that attracts objects towards each other, especially toward the center of the Earth. It causes things to fall and keeps planets orbiting around stars.
```

**primed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Gravity is a fundamental force of nature that attracts all objects with mass towards each other. It causes planets to orbit stars and gives weight to objects on Earth. The strength of gravity decreases with distance from the source of gravity (like the sun or moon), making it stronger closer to massive bodies like planets and stars.
```

### vaccine

> Explain what a vaccine does.

**zero_shot** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
A vaccine is a biological preparation that uses weakened or killed pathogens to stimulate the immune system to produce an immune response and create immunity against specific diseases. When a person receives a vaccine, their body produces antibodies that can recognize and fight off the actual pathogen if they encounter it in the future. This helps prevent serious illness and complications from certain infectious diseases.
```

**full** — content=0.67 conformance=0.67 (second_person=PASS, no_contractions=PASS, bulleted_list=x)

```
A vaccine works by helping your body build immunity against diseases without causing illness. - Vaccines introduce weakened or inactive parts of a virus or bacteria into your body. - Your immune system recognizes these components and creates antibodies to fight them off. - This prepares your body to recognize and defend against real infections if you come into contact with the actual pathogen later on.
```

**compressed** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
A vaccine works by introducing a small amount of weakened or inactive form of a virus or bacteria to stimulate the immune system without causing full-blown infection. This process helps the body build immunity against the disease. When exposed to the actual pathogen later, the vaccinated individual's immune system recognizes it quickly and mounts an effective defense, preventing illness or reducing its severity.
```

**style_text** — content=1.00 conformance=0.67 (second_person=PASS, no_contractions=PASS, bulleted_list=x)

```
A vaccine works by introducing a small amount of weakened or inactive parts of a virus or bacteria to your body. This helps your immune system recognize and prepare to fight off the real infection if it ever comes along. Essentially, vaccines teach your body how to protect itself against diseases without causing illness.
```

**primed** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
A vaccine works by introducing a small amount of weakened or inactive form of a virus or bacteria to stimulate the immune system without causing full-blown infection. This process helps the body build immunity against the disease. When exposed to the actual pathogen later, the vaccinated individual's immune system recognizes it quickly and mounts an effective defense, preventing illness or reducing its severity.
```

### tides

> Explain what causes ocean tides.

**zero_shot** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Ocean tides are caused by the gravitational pull of the moon and the sun on the Earth's oceans. The gravitational force exerted by these celestial bodies creates bulges in the water near their respective sides of the Earth - one high tide and one low tide. These tidal forces cause the oceans to move and create rhythmic patterns that we observe as tides. Additionally, the shape of the Earth's crust also plays a role in creating different tidal ranges at various locations around the world.
```

**full** — content=1.00 conformance=0.33 (second_person=x, no_contractions=x, bulleted_list=PASS)

```
- The gravitational pull from the moon and sun causes ocean tides.
- As these celestial bodies move through space, they exert force on Earth's oceans.
- This force creates two high tides per day: one at the rising tide and another at the falling tide.
- The difference between these high tides is known as the tidal range.
- Understanding this process helps us predict and manage coastal activities like fishing and shipping.
```

**compressed** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Ocean tides are caused by the gravitational pull of the moon and the sun on the Earth's oceans. The gravitational force exerted by these celestial bodies creates tidal bulges in the water, which then move back and forth as they rotate around the Earth. This results in two high tides and two low tides each day, creating the familiar ebb and flow of sea levels that we observe at the beach or in our local harbor.
```

**style_text** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Ocean tides are caused by the gravitational pull of the moon and the sun on Earth's oceans. The combined effect of these two celestial bodies creates a tidal force that causes the water to move up and down along the coastlines. This movement is periodic and can be observed as high and low tides.
```

**primed** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Ocean tides are caused by the gravitational pull of the moon and the sun on the Earth's oceans. The gravitational force exerted by these celestial bodies creates bulges in the water near the Earth's equator and at the poles. As the Earth rotates, these bulges move away from each other, creating two high tides per day (one at the equator and one at the poles) and two low tides. This periodic rise and fall of sea levels is what we observe as tidal cycles.
```

### friction

> Explain what friction is.

**zero_shot** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Friction is the force that resists the relative motion of solid surfaces, fluid layers, and material elements sliding against each other. It occurs whenever two objects in contact move or try to move relative to each other. Friction can be either static (resisting the start of movement) or kinetic (resisting the ongoing motion). The amount of friction depends on factors such as surface roughness, materials, temperature, and normal pressure between the contacting surfaces.
```

**full** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Friction is the force that resists the relative motion of solid surfaces, fluid layers, and material elements sliding against each other. - It occurs whenever there's a contact between two objects moving or trying to move past each other. - The more rough the surfaces, the greater the frictional force becomes. - Friction helps prevent slipping and allows us to walk without falling.
```

**compressed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Friction is a force that opposes the relative motion of objects sliding against each other. It occurs when two surfaces in contact move over one another and resist their separation. Friction arises due to the irregularities on the surfaces, which create microscopic interactions between particles at the point of contact. These interactions result in resistance to movement, causing the objects to slow down or stop. The amount of friction depends on factors such as the materials involved, the normal force pressing them together, and the roughness of the surfaces.
```

**style_text** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Friction: When two surfaces come into contact and move against each other, they create resistance to motion. This force opposes the relative motion of objects sliding or rubbing together. Friction can be beneficial, such as when it helps wheels roll smoothly on a surface, but it can also cause wear and tear if excessive.
```

**primed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Friction is the force that resists the relative motion of solid surfaces, fluid layers, and material elements sliding against each other. It occurs whenever there is a contact between two objects or materials moving over one another. Friction can be categorized as either static (when an object is at rest) or kinetic (when an object is in motion). The amount of friction depends on factors such as the types of surfaces in contact, their roughness, and the normal force pressing them together. Friction plays a crucial role in many everyday situations, from walking to driving vehicles, and it helps maintain stability in various mechanical systems.
```

### evaporation

> Explain what evaporation is.

**zero_shot** — content=1.00 conformance=0.00 (second_person=x, no_contractions=x, bulleted_list=x)

```
Evaporation is the process by which water changes from a liquid state to a gas (vapor) state. This occurs when water molecules gain enough energy to break free from the surface of a liquid and enter the air as vapor particles. The rate at which this happens depends on several factors including temperature, humidity, wind speed, and the presence of impurities in the water. Evaporation plays a crucial role in various natural processes such as precipitation, transpiration in plants, and cooling systems. It also contributes to climate regulation by removing heat from Earth's surface through the atmosphere.
```

**full** — content=1.00 conformance=0.33 (second_person=PASS, no_contractions=x, bulleted_list=x)

```
Evaporation is the process where a liquid turns into a gas. Imagine you have a glass of water on your desk. As the sun heats up the air around the glass, the water molecules near the surface gain enough energy to escape and turn into vapor. This means that more water molecules are now floating in the air instead of being on the surface of the water. Evaporation speeds up as the temperature increases because there's more heat available to give the molecules the energy they need to move away from the surface.
```

**compressed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Evaporation is the process where liquid substances turn into gases due to an increase in temperature and molecular motion. As the temperature rises, the kinetic energy of the molecules increases, causing them to move faster and escape from the surface of the liquid. This results in the formation of vapor or gas phase. The rate at which this occurs can be influenced by factors such as wind speed, air movement, and humidity levels.
```

**style_text** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Evaporation: Liquid turning into gas - molecules gain energy leaving surface. Speed increases with heat, leading to more noticeable changes.
```

**primed** — content=1.00 conformance=0.33 (second_person=x, no_contractions=PASS, bulleted_list=x)

```
Evaporation is the process where liquid substances turn into gases due to an increase in temperature and molecular motion. As the temperature rises, the kinetic energy of the molecules increases, causing them to move faster and escape from the surface of the liquid. This results in the formation of vapor or gas phase. The rate at which this occurs can be influenced by factors such as wind speed, humidity, and air pressure.
```
