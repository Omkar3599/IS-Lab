import hashlib
import random
import string
import time

def generate_random_strings(num_strings, length=20):
    """Generate a list of random alphanumeric strings."""
    strings = []
    for _ in range(num_strings):
        s = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        strings.append(s)
    return strings

def compute_hashes(strings, algorithm):
    """Compute hashes of strings using specified algorithm and measure time."""
    hash_func = getattr(hashlib, algorithm)
    hashes = []
    start = time.perf_counter()
    for s in strings:
        h = hash_func(s.encode()).hexdigest()
        hashes.append(h)
    end = time.perf_counter()
    duration = end - start
    return hashes, duration

def detect_collisions(hashes):
    """Detect collisions in a list of hash values."""
    seen = set()
    collisions = 0
    for h in hashes:
        if h in seen:
            collisions += 1
        else:
            seen.add(h)
    return collisions

def main():
    # Generate between 50 and 100 random strings of length 20
    num_strings = random.randint(50, 100)
    print(f"Generating {num_strings} random strings...")

    dataset = generate_random_strings(num_strings)

    algorithms = ['md5', 'sha1', 'sha256']

    for algo in algorithms:
        print(f"\nHashing with {algo.upper()}...")
        hashes, duration = compute_hashes(dataset, algo)
        collisions = detect_collisions(hashes)
        print(f"Time taken: {duration:.6f} seconds")
        print(f"Number of collisions detected: {collisions}")

if __name__ == "__main__":
    main()
