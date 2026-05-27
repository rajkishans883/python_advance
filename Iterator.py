"""
COMPLETE GUIDE TO ITERATORS IN PYTHON
Everything you need to know with examples
"""

# ============================================================================
# 1. WHAT IS AN ITERATOR?
# ============================================================================
# An iterator is an object that implements two methods: __iter__() and __next__()

class SimpleIterator:
    """Basic iterator that counts from 1 to n"""
    def __init__(self, max_num):
        self.max_num = max_num
        self.current = 0
    
    def __iter__(self):
        # Returns the iterator object itself
        # This allows the object to be used in for loops
        return self
    
    def __next__(self):
        # Returns the next value
        # Raises StopIteration when done
        self.current += 1
        if self.current > self.max_num:
            raise StopIteration
        return self.current

# Using our custom iterator
print("=== Custom Iterator ===")
counter = SimpleIterator(3)
for num in counter:
    print(num)  # Prints: 1, 2, 3


# ============================================================================
# 2. ITERATOR vs ITERABLE
# ============================================================================
# ITERABLE: Object that can return an iterator (has __iter__ method)
# ITERATOR: Object that produces values one at a time (has __iter__ AND __next__)

# List is ITERABLE but NOT an iterator
my_list = [1, 2, 3]

# Get an iterator from the iterable
list_iterator = iter(my_list)  # Calls __iter__()

print("\n=== Iterator vs Iterable ===")
print(next(list_iterator))  # 1
print(next(list_iterator))  # 2
print(next(list_iterator))  # 3
# print(next(list_iterator))  # Would raise StopIteration


# ============================================================================
# 3. BUILT-IN ITERABLES
# ============================================================================
print("\n=== Built-in Iterables ===")

iterables = {
    'list': [1, 2, 3],
    'tuple': (1, 2, 3),
    'string': "abc",
    'dict': {'a': 1, 'b': 2},
    'set': {1, 2, 3},
    'range': range(3),
    'file': None  # open('file.txt') would be an iterable
}

for name, obj in iterables.items():
    if obj is not None:
        print(f"{name}: {list(obj)}")


# ============================================================================
# 4. StopIteration EXCEPTION
# ============================================================================
print("\n=== StopIteration Exception ===")

numbers = [1, 2, 3]
num_iter = iter(numbers)

try:
    print(next(num_iter))  # 1
    print(next(num_iter))  # 2
    print(next(num_iter))  # 3
    print(next(num_iter))  # Raises StopIteration
except StopIteration:
    print("No more items!")


# ============================================================================
# 5. ITERATORS ARE LAZY (Memory Efficient)
# ============================================================================
# Iterators generate values on-demand, not all at once

import sys

print("\n=== Iterator Memory Efficiency ===")

# List stores all values in memory
big_list = [x for x in range(1000000)]
print(f"List size: {sys.getsizeof(big_list)} bytes")

# Range is an iterator - doesn't store all values
big_range = range(1000000)
print(f"Range size: {sys.getsizeof(big_range)} bytes")


# ============================================================================
# 6. ITERATORS ARE EXHAUSTIBLE
# ============================================================================
print("\n=== Iterators Are Exhaustible ===")

my_iter = iter([1, 2, 3])
print("First loop:", list(my_iter))   # [1, 2, 3]
print("Second loop:", list(my_iter))  # [] - Empty! Iterator exhausted

# To reuse, create a new iterator
my_list = [1, 2, 3]
print("Fresh iterator:", list(iter(my_list)))  # [1, 2, 3]


# ============================================================================
# 7. CUSTOM ITERATOR WITH STATE
# ============================================================================
class Fibonacci:
    """Iterator that generates Fibonacci sequence"""
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result

print("\n=== Fibonacci Iterator ===")
fib = Fibonacci(10)
print(list(fib))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# ============================================================================
# 8. iter() WITH SENTINEL VALUE
# ============================================================================
# iter(callable, sentinel) - calls callable until it returns sentinel

print("\n=== iter() with Sentinel ===")

counter_val = 0
def count_up():
    global counter_val
    counter_val += 1
    return counter_val

# Stop when count_up() returns 5
sentinel_iter = iter(count_up, 5)
print(list(sentinel_iter))  # [1, 2, 3, 4]


# ============================================================================
# 9. ITERATOR PROTOCOL IN CLASSES
# ============================================================================
class Countdown:
    """Iterable class that returns a new iterator each time"""
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        # Returns a NEW iterator object
        return CountdownIterator(self.start)

class CountdownIterator:
    """Separate iterator class"""
    def __init__(self, start):
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

print("\n=== Reusable Iterable ===")
countdown = Countdown(3)
print("First:", list(countdown))   # [3, 2, 1]
print("Second:", list(countdown))  # [3, 2, 1] - Works again!


# ============================================================================
# 10. COMMON ITERATOR FUNCTIONS
# ============================================================================
print("\n=== Iterator Functions ===")

from itertools import islice, cycle, count, chain

# islice - slice an iterator (doesn't load all into memory)
numbers = range(100)
print("First 5:", list(islice(numbers, 5)))

# cycle - infinite iterator that cycles through values
colors = cycle(['red', 'green', 'blue'])
print("Cycle 7:", [next(colors) for _ in range(7)])

# count - infinite counter
counter = count(10, 2)  # Start at 10, step by 2
print("Count 5:", [next(counter) for _ in range(5)])

# chain - combine multiple iterables
combined = chain([1, 2], [3, 4], [5, 6])
print("Chained:", list(combined))


# ============================================================================
# 11. REVERSE ITERATION
# ============================================================================
print("\n=== Reverse Iteration ===")

class ReverseIterator:
    """Iterate a sequence in reverse"""
    def __init__(self, data):
        self.data = data
        self.index = len(data)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]

rev = ReverseIterator([1, 2, 3, 4, 5])
print(list(rev))  # [5, 4, 3, 2, 1]


# ============================================================================
# 12. CHECKING IF OBJECT IS ITERABLE/ITERATOR
# ============================================================================
print("\n=== Type Checking ===")

from collections.abc import Iterable, Iterator

test_objects = {
    'list': [1, 2, 3],
    'iter': iter([1, 2, 3]),
    'int': 42,
    'custom_iterator': SimpleIterator(5)
}

for name, obj in test_objects.items():
    is_iterable = isinstance(obj, Iterable)
    is_iterator = isinstance(obj, Iterator)
    print(f"{name:20} - Iterable: {is_iterable}, Iterator: {is_iterator}")


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================
print("\n" + "="*70)
print("KEY POINTS TO REMEMBER:")
print("="*70)
print("""
1. Iterator must have __iter__() and __next__() methods
2. __iter__() returns self (the iterator object)
3. __next__() returns next value or raises StopIteration
4. Iterators are LAZY - values generated on demand (memory efficient)
5. Iterators are EXHAUSTIBLE - can only iterate once
6. Iterables return iterators via __iter__() or iter()
7. Use iter(iterable) to get iterator from iterable
8. Use next(iterator) to manually get next value
9. for loop automatically handles StopIteration
10. All iterators are iterables, but not all iterables are iterators
""")