import random
import math

# Extended Euclidean Algorithm for modular inverse
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def is_prime(n, k=10):
    """Miller-Rabin primality test"""
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11]:
        if n == p:
            return True
        if n % p == 0:
            return False
    s, d = 0, n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bitsize):
    while True:
        p = random.getrandbits(bitsize)
        p |= (1 << bitsize - 1) | 1  # Ensure high bit and oddness
        if is_prime(p):
            return p

class RSA:
    def __init__(self, bitsize=512):
        self.p = generate_prime(bitsize // 2)
        self.q = generate_prime(bitsize // 2)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 65537  # Common choice for e
        # Ensure e and phi(n) are coprime
        if math.gcd(self.e, self.phi) != 1:
            # Find an alternative e
            for candidate in range(3, 10000, 2):
                if math.gcd(candidate, self.phi) == 1:
                    self.e = candidate
                    break
        self.d = modinv(self.e, self.phi)

    def encrypt(self, m):
        if not (0 <= m < self.n):
            raise ValueError("Message out of range")
        return pow(m, self.e, self.n)

    def decrypt(self, c):
        return pow(c, self.d, self.n)

# Example usage
rsa = RSA(bitsize=512)

m1 = 7
m2 = 3

print(f"Original messages: {m1}, {m2}")

c1 = rsa.encrypt(m1)
c2 = rsa.encrypt(m2)

print(f"Ciphertext c1: {c1}")
print(f"Ciphertext c2: {c2}")

# Homomorphic multiplication: multiply ciphertexts mod n
c_product = (c1 * c2) % rsa.n

print(f"Ciphertext of product (c1 * c2 mod n): {c_product}")

# Decrypt the product
decrypted_product = rsa.decrypt(c_product)

print(f"Decrypted product: {decrypted_product}")

# Verify correctness
print(f"Product of plaintexts: {m1 * m2}")
print(f"Verification passed: {decrypted_product == m1 * m2}")
