def letter_to_num(c):
    # Capital letter mapping: A=0,...,Z=25
    return ord(c.upper()) - ord('A')

def num_to_letter(n):
    # Map number back to capital letter
    return chr((n % 26) + ord('A'))

def hill_encrypt(plaintext, key):
    # Remove spaces and make uppercase
    raw = ''.join([c for c in plaintext.upper() if c.isalpha()])
    # Pad with X if needed
    if len(raw) % 2 == 1:
        raw += 'X'
    ciphertext = ''
    for i in range(0, len(raw), 2):
        # Block of 2 letters
        a = letter_to_num(raw[i])
        b = letter_to_num(raw[i+1])
        # Matrix multiplication mod 26
        c1 = (key[0][0] * a + key[0][1] * b) % 26
        c2 = (key[1][0] * a + key[1][1] * b) % 26
        ciphertext += num_to_letter(c1) + num_to_letter(c2)
    return ciphertext

# Define key matrix as per the question
key = [[3, 3], [2, 7]]
msg = input("Enter the message: ")
cipher = hill_encrypt(msg, key)
print(cipher)
