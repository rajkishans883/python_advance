# generator.py
"""
Comprehensive Python Generator Examples
Generators are memory-efficient iterators that generate values on-the-fly.
They use 'yield' instead of 'return' and maintain their state between calls.
"""

def simple_generator():
    """Basic generator demonstrating state maintenance"""
    print("Generator started")
    yield "First value"
    print("After first yield")
    yield "Second value"
    print("Generator ending")
    return "Generator complete"  # This will raise StopIteration with this value

def countdown(n):
    """Countdown generator"""
    while n > 0:
        yield n
        n -= 1
    yield "Blast off!"

def squares(n):
    """Generate squares of numbers up to n"""
    for i in range(1, n+1):
        yield i * i

def prime_numbers():
    """Infinite generator of prime numbers"""
    yield 2
    primes = [2]
    num = 3
    while True:
        if all(num % p != 0 for p in primes):
            primes.append(num)
            yield num
        num += 2

def data_processor(data):
    """Generator for processing data in chunks"""
    chunk_size = 2
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def tree_traversal(node):
    """Generator for tree traversal (simplified example)"""
    yield node['value']
    for child in node.get('children', []):
        yield from tree_traversal(child)

def coroutine_example():
    """Generator as a coroutine (can receive values)"""
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

def main():
    # Example 1: Basic generator with state
    print("\n=== Basic Generator ===")
    gen = simple_generator()
    print(next(gen))  # First value
    print(next(gen))  # Second value
    try:
        print(next(gen))  # Will raise StopIteration
    except StopIteration as e:
        print(f"Generator returned: {e.value}")

    # Example 2: Countdown
    print("\n=== Countdown ===")
    for num in countdown(5):
        print(num)

    # Example 3: Squares generator
    print("\n=== Squares Generator ===")
    print(list(squares(5)))  # [1, 4, 9, 16, 25]

    # Example 4: Prime numbers (first 10)
    print("\n=== Prime Numbers ===")
    primes = prime_numbers()
    for _ in range(10):
        print(next(primes))

    # Example 5: Data processing in chunks
    print("\n=== Data Chunking ===")
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    for chunk in data_processor(data):
        print(f"Processing chunk: {chunk}")

    # Example 6: Tree traversal
    print("\n=== Tree Traversal ===")
    tree = {
        'value': 1,
        'children': [
            {'value': 2, 'children': [{'value': 4}, {'value': 5}]},
            {'value': 3, 'children': [{'value': 6}]}
        ]
    }
    for value in tree_traversal(tree):
        print(value)

    # Example 7: Generator as coroutine
    print("\n=== Coroutine Example ===")
    accum = coroutine_example()
    next(accum)  # Prime the generator
    print(accum.send(10))  # 10
    print(accum.send(20))  # 30
    print(accum.send(5))   # 35
    accum.close()  # Properly close the coroutine

    # Example 8: Generator expression
    print("\n=== Generator Expression ===")
    gen_exp = (x**2 for x in range(5))
    print(list(gen_exp))  # [0, 1, 4, 9, 16]

    # Example 9: Memory efficiency comparison
    print("\n=== Memory Efficiency ===")
    import sys

    # Regular list
    big_list = [i for i in range(100000)]
    print(f"List size: {sys.getsizeof(big_list)} bytes")

    # Generator
    big_gen = (i for i in range(100000))
    print(f"Generator size: {sys.getsizeof(big_gen)} bytes")

if __name__ == "__main__":
    main()