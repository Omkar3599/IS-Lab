import binascii

# Initial permutation table
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17,  9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Final permutation table
FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41,  9, 49, 17, 57, 25]

# Expansion table
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# Permutation function P
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# S-boxes (S1 to S8)
S_boxes = [
  # S1
  [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
   [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
   [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
   [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
  # S2
  [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
   [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
   [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
   [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
  # S3
  [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
   [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
   [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
   [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
  # S4
  [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
   [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
   [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
   [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
  # S5
  [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
   [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
   [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
   [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
  # S6
  [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
   [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
   [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
   [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
  # S7
  [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
   [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
   [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
   [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
  # S8
  [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
   [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
   [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
   [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]

# Convert text (bytes) to 64-bit binary

def text_to_bits(text8):
    return ''.join(format(b, '08b') for b in text8)

# Convert 64-bit binary to bytes
def bits_to_bytes(bits):
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

# Permute bits according to table
def permute(block, table):
    return ''.join([block[i-1] for i in table])

# S-box substitution
def substitute(bits):
    result = ''
    for i in range(8):
        block = bits[i*6:(i+1)*6]
        row = int(block[0] + block[-1], 2)
        col = int(block[1:5], 2)
        val = S_boxes[i][row][col]
        result += bin(val)[2:].zfill(4)
    return result

# DES round function
def feistel(right, subkey):
    right_expanded = permute(right, E)
    xored = bin(int(right_expanded, 2) ^ int(subkey, 2))[2:].zfill(48)
    substituted = substitute(xored)
    return permute(substituted, P)

# Simplified key schedule
def generate_round_keys(key):
    key_bits = text_to_bits(key.encode().ljust(8, b'\0'))[:56]
    round_keys = []
    for i in range(16):
        rotated = key_bits[i:] + key_bits[:i]
        round_keys.append(rotated[:48])
    return round_keys

# DES encryption/decryption for one 64-bit block
def des_block(block, key, encrypt=True):
    block_bits = text_to_bits(block)
    block_bits = permute(block_bits, IP)
    left, right = block_bits[:32], block_bits[32:]

    round_keys = generate_round_keys(key)
    if not encrypt:
        round_keys.reverse()

    for rk in round_keys:
        new_right = bin(int(left, 2) ^ int(feistel(right, rk), 2))[2:].zfill(32)
        left, right = right, new_right

    combined = right + left
    return permute(combined, FP)

# Pad plaintext to multiple of 8 bytes
def pad(data):
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len]) * pad_len

# Unpad

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

# DES encrypt

def des_encrypt(plaintext, key):
    data = pad(plaintext.encode())
    result = b''
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        encrypted_bits = des_block(block, key, True)
        result += bits_to_bytes(encrypted_bits)
    return result

# DES decrypt
def des_decrypt(ciphertext, key):
    result = b''
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        decrypted_bits = des_block(block, key, False)
        result += bits_to_bytes(decrypted_bits)
    return unpad(result).decode(errors='ignore')

# Test
plaintext = input("Enter plain text: ")
key = "A1B2C3D4"

cipher = des_encrypt(plaintext, key)
print("Ciphertext (hex):", cipher.hex().upper())

decrypted = des_decrypt(cipher, key)
print("Decrypted text:", decrypted)
