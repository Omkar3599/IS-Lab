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
    e = 65537
    if gcd(e, phi) != 1:
        e = 3
    d = modinverse(e, phi)
    return (n, e), (n, d)

# Split message into chunks (each < n)
def chunk_message(msg, n):
    msg_bytes = msg.encode()
    chunk_size = (n.bit_length() - 1) // 8
    return [int.from_bytes(msg_bytes[i:i+chunk_size], 'big')
            for i in range(0, len(msg_bytes), chunk_size)]

# Encrypt each chunk
def encrypt_chunk(chunks, pubkey):
    n, e = pubkey
    return [power(c, e, n) for c in chunks]

# Decrypt each chunk
def decrypt_chunk(cipher_chunks, privkey):
    n, d = privkey
    msg_bytes = b''.join(
        (power(c, d, n)).to_bytes((n.bit_length() + 7) // 8, 'big').lstrip(b'\x00')
        for c in cipher_chunks
    )
    return msg_bytes.decode()

# Demo
if __name__ == "__main__":
    public_key, private_key = generate_key(bits=32)  # small for demo
    print("Public Key:", public_key)
    print("Private Key:", private_key)

    message = input("Enter: ")
    print("Original:", message)

    chunks = chunk_message(message, public_key[0])
    cipher_chunks = encrypt_chunk(chunks, public_key)
    decrypted = decrypt_chunk(cipher_chunks, private_key)

    print("Ciphertext (chunks):", cipher_chunks)
    print("Decrypted:", decrypted)
