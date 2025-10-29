import random
import math

# Utility functions

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def modinv(a, m):
    """Modular inverse using Extended Euclidean Algorithm"""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def extended_gcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def get_prime(bitsize):
    """Generate a prime number of approximately bitsize bits"""
    while True:
        num = random.getrandbits(bitsize)
        # Ensure num is odd and of correct bit length
        num |= (1 << bitsize - 1) | 1
        if is_prime(num):
            return num

def is_prime(n, k=10):
    """Miller-Rabin primality test"""
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11]:
        if n % p == 0 and n != p:
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

# Paillier key generation, encryption, and decryption

class Paillier:
    def __init__(self, bitsize=512):
        self.p = get_prime(bitsize // 2)
        self.q = get_prime(bitsize // 2)
        self.n = self.p * self.q
        self.nsquare = self.n * self.n
        self.g = self.n + 1
        self.lambda_param = lcm(self.p - 1, self.q - 1)
        # Compute mu = (L(g^lambda mod n^2))^-1 mod n
        x = pow(self.g, self.lambda_param, self.nsquare)
        self.mu = modinv(self.L(x), self.n)

    def L(self, u):
        return (u - 1) // self.n

    def encrypt(self, m):
        if not (0 <= m < self.n):
            raise ValueError("Message out of range")
        while True:
            r = random.randrange(1, self.n)
            if math.gcd(r, self.n) == 1:
                break
        c = (pow(self.g, m, self.nsquare) * pow(r, self.n, self.nsquare)) % self.nsquare
        return c

    def decrypt(self, c):
        if not (0 <= c < self.nsquare):
            raise ValueError("Ciphertext out of range")
        x = pow(c, self.lambda_param, self.nsquare)
        l = self.L(x)
        m = (l * self.mu) % self.n
        return m

    def e_add(self, c1, c2):
        """Homomorphic addition of ciphertexts"""
        return (c1 * c2) % self.nsquare

# Demonstration

paillier = Paillier(bitsize=512)

m1 = 15
m2 = 25

print(f"Original messages: {m1}, {m2}")

c1 = paillier.encrypt(m1)
c2 = paillier.encrypt(m2)

print(f"Ciphertext c1: {c1}")
print(f"Ciphertext c2: {c2}")

# Add encrypted messages (homomorphic addition)
c_sum = paillier.e_add(c1, c2)

print(f"Ciphertext of sum (c1 * c2 mod n^2): {c_sum}")

# Decrypt sum
decrypted_sum = paillier.decrypt(c_sum)

print(f"Decrypted sum: {decrypted_sum}")

# Verify correctness
print(f"Sum of plaintexts: {m1 + m2}")
print(f"Verification passed: {decrypted_sum == m1 + m2}")
