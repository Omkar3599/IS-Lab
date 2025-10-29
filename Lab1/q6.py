# Affine Cipher Brute Force Attack
# Known: plaintext "ab" -> ciphertext "GL"

def char_to_num(char):
    """Convert character to number (A=0, B=1, ..., Z=25)"""
    return ord(char.upper()) - ord('A')


def num_to_char(num):
    """Convert number to character (0=A, 1=B, ..., 25=Z)"""
    return chr((num % 26) + ord('A'))


def gcd(a, b):
    """Calculate greatest common divisor using Euclidean algorithm"""
    while b != 0:
        a, b = b, a % b
    return a


def mod_inverse(a, m):
    """Find modular inverse of a modulo m"""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def affine_encrypt(plaintext, a, b):
    """Encrypt using affine cipher E(x) = (a*x + b) mod 26"""
    result = []
    for char in plaintext:
        if char.isalpha():
            x = char_to_num(char)
            y = (a * x + b) % 26
            result.append(num_to_char(y))
        else:
            result.append(char)
    return ''.join(result)


def affine_decrypt(ciphertext, a, b):
    """Decrypt using affine cipher D(y) = a⁻¹*(y - b) mod 26"""
    result = []
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return None

    for char in ciphertext:
        if char.isalpha():
            y = char_to_num(char)
            x = (a_inv * (y - b)) % 26
            result.append(num_to_char(x))
        else:
            result.append(char)
    return ''.join(result)


# Known plaintext-ciphertext pair
known_plain = "ab"
known_cipher = "GL"

print("Known plaintext-ciphertext pair:")
print(f"Plaintext: {known_plain}")
print(f"Ciphertext: {known_cipher}")

p1, p2 = char_to_num('a'), char_to_num('b')
c1, c2 = char_to_num('G'), char_to_num('L')

# Equations: (a*0 + b) ≡ 6 mod 26, (a*1 + b) ≡ 11 mod 26
b = c1  # b = 6
a = (c2 - b) % 26  # a = (11 - 6) = 5

print(f"Calculated parameters: a = {a}, b = {b}")

# Verify the parameters work
test_result = affine_encrypt(known_plain, a, b)
print(f"Verification: '{known_plain}' encrypts to '{test_result}' (should be '{known_cipher}')")

# Decrypt the message
ciphertext = "XPALASXYFGFUKPXUSOGEUTKCDGEXANMGNVS"
decrypted = affine_decrypt(ciphertext, a, b)
print(f"\nDecrypted message: {decrypted}")
