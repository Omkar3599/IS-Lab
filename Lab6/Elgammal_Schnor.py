import random

# Fast modular exponentiation
def power(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

# Euclidean GCD
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Extended Euclidean Algorithm for modular inverse
def modinverse(e, phi):
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise Exception("Modular inverse does not exist")
    return x % phi

# Check primality (basic Miller-Rabin)
def is_prime(n, k=5):
    if n < 2:
        return False
    if n in [2, 3]:
        return True
    if n % 2 == 0:
        return False

    # write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = power(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = power(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Generate prime of given bit length
def generate_prime(bits=16):
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p

# Generate RSA keypair
def generate_key(bits=16):
    p = generate_prime(bits)
    q = generate_prime(bits)
    while p == q:
        q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # 0x10001, standard public exponent
    if gcd(e, phi) != 1:
        # fallback if gcd != 1
        for candidate in [3, 5, 17, 257]:
            if gcd(candidate, phi) == 1:
                e = candidate
                break
    d = modinverse(e, phi)
    return (n, e), (n, d)

# Hash function (simple SHA-256 wrapper)
import hashlib
def hash_message(message):
    return int(hashlib.sha256(message.encode()).hexdigest(), 16)

# Sign message with private key
def sign_message(message, privkey):
    n, d = privkey
    hashed = hash_message(message) % n  # Take hash mod n
    signature = power(hashed, d, n)
    return signature

def verify_signature(message, signature, pubkey):
    n, e = pubkey
    hashed = hash_message(message) % n  # Take hash mod n
    hashed_from_signature = power(signature, e, n)
    return hashed == hashed_from_signature


# Demo simulating Alice and Bob's digital signature exchange
if __name__ == "__main__":
    print("Generating Alice's RSA keys...")
    alice_pub, alice_priv = generate_key(16)
    print(f"Alice Public Key (n, e): {alice_pub}")
    print(f"Alice Private Key (n, d): {alice_priv}")

    print("\nGenerating Bob's RSA keys...")
    bob_pub, bob_priv = generate_key(16)
    print(f"Bob Public Key (n, e): {bob_pub}")
    print(f"Bob Private Key (n, d): {bob_priv}")

    # Alice signs a document
    alice_message = "This is Alice's legal document."
    print(f"\nAlice signs message: '{alice_message}'")
    alice_signature = sign_message(alice_message, alice_priv)
    print(f"Alice's Signature: {alice_signature}")

    # Bob verifies Alice's signature
    print("\nBob verifies Alice's signature...")
    if verify_signature(alice_message, alice_signature, alice_pub):
        print("Signature verified! It's Alice's signature.")
    else:
        print("Signature verification failed!")

    # Bob signs his own message
    bob_message = "THIS IS BOB'S LEGAL DOCUMENT."
    print(f"\nBob signs message: '{bob_message}'")
    bob_signature = sign_message(bob_message, bob_priv)
    print(f"Bob's Signature: {bob_signature}")

    # Alice verifies Bob's signature
    print("\nAlice verifies Bob's signature...")
    if verify_signature(bob_message, bob_signature, bob_pub):
        print("Signature verified! It's Bob's signature.")
    else:
        print("Signature verification failed!")

