from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

# AES-128 key (16 bytes = 128 bits)
key = bytes.fromhex("0123456789ABCDEF0123456789ABCDEF")

# AES requires block size of 16 bytes
plaintext = "Sensitive Information".encode()

# Create AES cipher in ECB mode
cipher = AES.new(key, AES.MODE_ECB)

# Encrypt with padding
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
print("Ciphertext (hex):", binascii.hexlify(ciphertext).upper().decode())

# Decrypt
decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
print("Decrypted text:", decrypted.decode())
