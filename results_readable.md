# Primer harness run (multi-domain, split=test)

## Overall

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| full | 0.96 | 0.61 | 209 |
| compressed | 0.89 | 0.42 | 114 |
| style_text | 0.85 | 0.58 | 163 |
| primed | 1.00 | 0.50 | 114 |

## Domain: coding

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| full | 1.00 | 0.75 | 235 |
| compressed | 0.67 | 0.67 | 107 |
| style_text | 0.67 | 0.83 | 150 |
| primed | 1.00 | 0.75 | 107 |

### dedupe_preserve_order

> Write a function `dedupe(items: list) -> list` that removes duplicates while preserving first-seen order.

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

**primed** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
def dedupe(items: list) -> list:
    """Remove duplicates from a list while preserving first-seen order.
    
    Args:
        items (list): A list of items to remove duplicates from.
        
    Returns:
        list: A new list with duplicates removed.
    """
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]
```
```

### word_frequencies

> Write a function `word_freq(text: str) -> dict` mapping each lowercased word to its count.

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
from typing import Dict

def word_freq(text: str) -> Dict[str, int]:
    """
    Counts the frequency of each lowercase word in the given text.
    
    >>> word_freq("Hello world! Hello again.")
    {'hello': 2, 'world': 1}
    >>> word_freq("Python is fun")
    {'python': 1, 'is': 1, 'fun': 1}
    """

    # Convert text to lowercase and split into words
    words = text.lower().split()

    # Use a dictionary comprehension to count occurrences of each word
    return {word: words.count(word) for word in words}
```
```

### running_max

> Write a function `running_max(nums: list) -> list` returning the cumulative maximum at each index.

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

**primed** — content=1.00 conformance=0.75 (snake_case=PASS, type_hints=PASS, raises_valueerror=x, docstring=PASS)

```
```python
from typing import List

def running_max(nums: List[int]) -> List[int]:
    """
    Calculate the cumulative maximum of a given list of integers.
    
    Args:
        nums (List[int]): A list of integers.
        
    Returns:
        List[int]: A list containing the cumulative maximum at each index.
    """
    return [max(nums[:i+1]) for i in range(len(nums))]
```
```

## Domain: math

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| full | 1.00 | 0.75 | 224 |
| compressed | 1.00 | 0.50 | 152 |
| style_text | 1.00 | 0.67 | 195 |
| primed | 1.00 | 0.50 | 152 |

### share_candy

> There are 24 candies shared equally among 6 children. How many candies does each child get?

**full** — content=1.00 conformance=0.50 (numbered_steps=x, shows_arithmetic=PASS, answer_line=x, no_prose_intro=PASS)

```
Step 1: Divide total candies by number of children = 24 / 6 = 4
Answer: Each child gets 4 candies.
```

**compressed** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=PASS)

```
Step 1: Divide the total number of candies by the number of children to find out how many candies each child gets.
24 ÷ 6 = 4

Answer: Each child gets 4 candies.
```

**style_text** — content=1.00 conformance=0.50 (numbered_steps=PASS, shows_arithmetic=x, answer_line=x, no_prose_intro=PASS)

```
Step 1: Divide the total number of candies by the number of children to find out how many candies each child gets.
Step 2: 24 ÷ 6 = 4 candies per child. Answer: 4 candies.
```

**primed** — content=1.00 conformance=0.25 (numbered_steps=x, shows_arithmetic=x, answer_line=x, no_prose_intro=PASS)

```
Step 1: 24 ÷ 6 = 4 candies per child. Answer: Each child gets 4 candies.
```

### discount_price

> A shirt costs 20 dollars and has a 10 percent discount. What is the final price in dollars?

**full** — content=1.00 conformance=0.75 (numbered_steps=PASS, shows_arithmetic=PASS, answer_line=x, no_prose_intro=PASS)

```
Step 1: Calculate the discount amount.
   Step 1a: Multiply original price by discount rate.
      Answer: \( 20 \times 0.10 = 2 \)

Step 2: Subtract the discount from the original price to find the final price.
   Step 2a: Subtract discount from original price.
      Answer: \( 20 - 2 = 18 \)

Final answer: The final price of the shirt is $18.
```

**compressed** — content=1.00 conformance=0.50 (numbered_steps=PASS, shows_arithmetic=x, answer_line=x, no_prose_intro=PASS)

```
Step 1: Calculate the discount amount on the shirt.
The original price of the shirt is $20, and there is a 10% discount.
Discount amount = Original price × Discount rate
Discount amount = $20 × 10%
Discount amount = $2

Step 2: Subtract the discount from the original price to find the final price.
Final price = Original price - Discount amount
Final price = $20 - $2
Final price = $18

Answer: The final price of the shirt after applying the 10% discount is $18.
```

**style_text** — content=1.00 conformance=0.50 (numbered_steps=PASS, shows_arithmetic=x, answer_line=x, no_prose_intro=PASS)

```
Step 1: Calculate the discount amount.
   Discount = Original Price × Discount Rate
            = $20 × 10%
            = $20 × 0.10
            = $2

Step 2: Subtract the discount from the original price to find the final price.
   Final Price = Original Price - Discount
               = $20 - $2
               = $18

Answer: The final price of the shirt is $18.
```

**primed** — content=1.00 conformance=0.50 (numbered_steps=PASS, shows_arithmetic=x, answer_line=x, no_prose_intro=PASS)

```
Step 1: Calculate the discount amount on the shirt.
   Discount amount = Original price × Discount rate
                    = $20 × 10%
                    = $20 × 0.10
                    = $2

Step 2: Subtract the discount from the original price to get the final price.
   Final price = Original price - Discount amount
               = $20 - $2
               = $18

Answer: The final price of the shirt after applying the 10% discount is $18.
```

### pages_left

> A book has 120 pages. Ada read 45 pages on Monday and 35 on Tuesday. How many pages are left?

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
Step 1: Calculate the total number of pages Ada read so far.
Ada read 45 pages on Monday and 35 pages on Tuesday.
Total pages read = 45 + 35

Step 2: Subtract the total pages read from the initial number of pages in the book to find out how many pages are left.
Pages left = Total pages in the book - Total pages read

Let's perform these calculations:

Step 1:
45 (Monday) + 35 (Tuesday) = 80 pages

Step 2:
120 (total pages in the book) - 80 (pages read) = 40 pages

Answer: There are 40 pages left in the book.
```

## Domain: writing

| arm | content | conformance | avg_tokens |
|---|---|---|---|
| full | 0.89 | 0.33 | 167 |
| compressed | 1.00 | 0.08 | 84 |
| style_text | 0.89 | 0.25 | 145 |
| primed | 1.00 | 0.25 | 84 |

### gravity

> Explain what gravity is.

**full** — content=1.00 conformance=0.25 (british_spelling=x, second_person=x, no_contractions=PASS, bulleted_list=x)

```
Gravity is the force that attracts objects with mass towards each other. It causes things to fall down and keeps planets orbiting around stars. The more massive an object is, the stronger its gravitational pull becomes.
```

**compressed** — content=1.00 conformance=0.00 (british_spelling=x, second_person=x, no_contractions=x, bulleted_list=x)

```
Gravity is a fundamental force of nature that attracts all objects with mass towards each other. It causes planets, stars, and galaxies to orbit around centers of mass, such as the sun in our solar system. On Earth, gravity pulls objects downward toward the planet's center, giving rise to the familiar sensation of weight. This force also governs the motion of tides on oceans and the paths of projectiles like thrown balls or bullets.
```

**style_text** — content=1.00 conformance=0.25 (british_spelling=x, second_person=x, no_contractions=PASS, bulleted_list=x)

```
Gravity: The force that attracts objects towards each other, especially those of different masses. It pulls everything on Earth toward its center, causing things to fall down and making planets orbit around stars. This fundamental force governs much of our daily lives and celestial movements.
```

**primed** — content=1.00 conformance=0.25 (british_spelling=x, second_person=x, no_contractions=PASS, bulleted_list=x)

```
Gravity is the force that attracts two objects with mass towards each other. It causes things to fall down and keeps planets in orbit around stars. The strength of gravity depends on the masses of the objects involved and the distance between them.
```

### vaccine

> Explain what a vaccine does.

**full** — content=0.67 conformance=0.25 (british_spelling=x, second_person=PASS, no_contractions=x, bulleted_list=x)

```
A vaccine works by introducing your body's immune system to a harmless version of a disease-causing microorganism or part of that organism. This helps your body build immunity without causing illness. Essentially, vaccines teach your immune system how to recognize and fight off specific diseases before you encounter them naturally.
```

**compressed** — content=1.00 conformance=0.00 (british_spelling=x, second_person=x, no_contractions=x, bulleted_list=x)

```
A vaccine works by introducing a small amount of weakened or inactive form of a pathogen (such as a virus or bacteria) into the body. This allows the immune system to recognize and build immunity against that specific pathogen without causing full-blown illness. The process involves several key steps:

1. **Introduction**: A tiny dose of the pathogen is injected into the body through various methods like injections or nasal sprays.
2. **Immune Response Initiation**: When the pathogen enters the body, it triggers an immune response. The immune system recognizes this foreign substance and begins to produce antibodies specifically targeted against it.
3. **Memory Formation**: Over time, the immune system stores information about how to fight off future encounters with the same pathogen. This stored knowledge becomes part of the body's memory, allowing for quicker and more effective responses in case of real infection.
4. **Protection Against Future Infections**: By creating these protective antibodies and memory cells, vaccines provide long-lasting immunity against diseases caused by the specific pathogens they target. This means individuals who have received a vaccine can generally avoid contracting certain illnesses if exposed to them later in life.

Vaccines play a crucial role in preventing infectious diseases by preparing the body’s defenses before exposure to actual pathogens, thereby reducing the risk of severe illness and complications associated with many common and potentially deadly infections.
```

**style_text** — content=0.67 conformance=0.25 (british_spelling=x, second_person=PASS, no_contractions=x, bulleted_list=x)

```
A vaccine works by introducing your body's immune system to a harmless version of a disease-causing microorganism or part of it. This triggers an immune response without causing illness, allowing your body to build immunity against that specific pathogen.
```

**primed** — content=1.00 conformance=0.25 (british_spelling=x, second_person=x, no_contractions=PASS, bulleted_list=x)

```
A vaccine works by introducing a weakened or inactive form of a pathogen (such as a virus or bacteria) into the body. This allows the immune system to recognize and build immunity against the specific microorganism without causing illness. The process involves several key steps:

1. **Introduction**: A small amount of the pathogen is administered through injection or oral intake.
2. **Immune Response Initiation**: When the pathogen enters the body, it triggers an immune response. 
3. **Activation of Immune Cells**: Specialized cells in the immune system detect the presence of the pathogen and activate other immune cells.
4. **Production of Antibodies**: These activated cells produce antibodies that specifically target the pathogen.
5. **Neutralization and Elimination**: The antibodies bind to the pathogen, neutralizing its ability to cause disease, thereby preventing infection.

This method ensures that the body develops protective immunity against the pathogen without experiencing the full effects of the actual infection, thus providing long-lasting protection.
```

### tides

> Explain what causes ocean tides.

**full** — content=1.00 conformance=0.50 (british_spelling=PASS, second_person=x, no_contractions=x, bulleted_list=PASS)

```
Explain what causes ocean tides.

- The gravitational pull from the moon and sun on Earth's oceans creates tidal forces.
- These forces cause the water levels around the coastlines to rise and fall periodically.
- This phenomenon is known as tides.
- The time between high tide and low tide varies depending on the location and the specific conditions.
```

**compressed** — content=1.00 conformance=0.25 (british_spelling=PASS, second_person=x, no_contractions=x, bulleted_list=x)

```
Ocean tides are caused by the gravitational pull of the moon and the sun on the Earth's oceans. The gravitational force exerted by these celestial bodies creates tidal bulges in the water, which then cause the oceans to rise and fall as they rotate around the Earth. This results in two high tides per day (one each side of the Earth) and two low tides. The strength of the tides can vary depending on factors such as the distance between the Earth, moon, and sun, as well as the shape of the Earth's crust.
```

**style_text** — content=1.00 conformance=0.25 (british_spelling=PASS, second_person=x, no_contractions=x, bulleted_list=x)

```
Ocean tides are caused by the gravitational pull of the moon and the sun on Earth's oceans. The combined effect of these two celestial bodies creates a tidal force that causes the water levels in the oceans to rise and fall periodically. This phenomenon is known as tidal motion. The shape of the coastline and the depth of the sea also play a role in determining how much the tide rises or falls.
```

**primed** — content=1.00 conformance=0.25 (british_spelling=PASS, second_person=x, no_contractions=x, bulleted_list=x)

```
Ocean tides occur due to the gravitational pull of the moon and the sun on the Earth's oceans. The combined effect of these two celestial bodies creates a tidal force that causes the water levels in coastal areas to rise and fall. This phenomenon is caused by the rotation of the Earth and the varying positions of the moon and sun relative to the Earth. As the moon orbits around the Earth, it pulls on the water near its side, creating high tides. At the opposite end of the orbit, the water recedes, resulting in low tides. These cycles repeat approximately every 12 hours and 25 minutes, creating a regular pattern of rising and falling sea levels along coastlines.
```
