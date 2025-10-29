from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii

# AES parameters
plaintext = b"Top Secret Data"
key_hex = "FEDCBA9876543210FEDCBA9876543210FEDCBA9876543210"  # 192-bit key
key = bytes.fromhex(key_hex)

# Create AES-192 cipher (ECB)
cipher = AES.new(key, AES.MODE_ECB)

# Encrypt
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
print("Plaintext:", plaintext.decode())
print("Key (192-bit):", key_hex)
print("Ciphertext (hex):", binascii.hexlify(ciphertext).upper().decode())

# Decrypt
decrypted = cipher.decrypt(ciphertext).decode().rstrip("\x04")  # unpad manually
print("Decrypted:", decrypted)
