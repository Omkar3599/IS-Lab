import random

# --- Helper functions ---
def power(base, exp, mod):
    """Fast modular exponentiation (base^exp mod mod)."""
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """Return modular inverse of a under modulo m."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# --- ElGamal Key Generation ---
def generate_keys():
    p = 30803                # prime modulus
    g = 2                    # generator
    x = random.randint(2, p-2)   # private key
    h = power(g, x, p)       # h = g^x mod p
    return (p, g, h), x      # (public key), private key

# --- Encryption ---
def encrypt(msg, public_key):
    p, g, h = public_key
    y = random.randint(1, p-2)          # random y
    c1 = power(g, y, p)                 # c1 = g^y mod p
    s = power(h, y, p)                  # s = h^y mod p
    ciphertext = [(c1, (ord(ch) * s) % p) for ch in msg]
    return ciphertext

# --- Decryption ---
def decrypt(ciphertext, private_key, p):
    decrypted = ""
    for c1, c2 in ciphertext:
        s = power(c1, private_key, p)       # s = c1^x mod p
        s_inv = mod_inverse(s, p)           # modular inverse
        decrypted += chr((c2 * s_inv) % p)  # recover message
    return decrypted

# --- Demo ---
if __name__ == "__main__":
    msg = "Confidential Data"
    public_key2, private_key2 = generate_keys()
    print("Public Key (p, g, h):", public_key2)
    print("Private Key x:", private_key2)

    ciphertext = encrypt(msg, public_key2)
    print("\nCiphertext:", ciphertext)

    decrypted_msg = decrypt(ciphertext, private_key2, public_key2[0])
    print("\nDecrypted:", decrypted_msg)
