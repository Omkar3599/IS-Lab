# Known-plaintext attack on shift cipher
# Given: "CIW" decrypts to "yes"
# Find shift key and decrypt "XVIEWYWI"

def char_to_num(char):
    """Convert character to number (A=0, B=1, ..., Z=25)"""
    return ord(char.upper()) - ord('A')


def num_to_char(num):
    """Convert number to character (0=A, 1=B, ..., 25=Z)"""
    return chr((num % 26) + ord('A'))


def find_shift_key(ciphertext, plaintext):
    """Find the shift key from known plaintext-ciphertext pair"""
    if len(ciphertext) != len(plaintext):
        return None

    shifts = []
    for i in range(len(ciphertext)):
        cipher_num = char_to_num(ciphertext[i])
        plain_num = char_to_num(plaintext[i])
        shift = (cipher_num - plain_num) % 26
        shifts.append(shift)

    # Check if all shifts are the same
    if all(s == shifts[0] for s in shifts):
        return shifts[0]
    return None


def decrypt_shift(ciphertext, shift):
    """Decrypt ciphertext using shift cipher"""
    result = []
    for char in ciphertext:
        if char.isalpha():
            cipher_num = char_to_num(char)
            plain_num = (cipher_num - shift) % 26
            result.append(num_to_char(plain_num))
        else:
            result.append(char)
    return ''.join(result)


# Known plaintext attack
ciphertext1 = "CIW"
plaintext1 = "YES"  # "yes" converted to uppercase
print(f"Known ciphertext: {ciphertext1}")
print(f"Known plaintext: {plaintext1}")

# Find the shift key
shift_key = find_shift_key(ciphertext1, plaintext1)
print(f"Shift key found: {shift_key} ({shift_key} or {-shift_key % 26})")

# New ciphertext to decrypt
ciphertext2 = "XVIEWYWI"
print(f"\nNew ciphertext: {ciphertext2}")

# Decrypt using the found shift key
decrypted = decrypt_shift(ciphertext2, shift_key)
print(f"Decrypted plaintext: {decrypted}")

