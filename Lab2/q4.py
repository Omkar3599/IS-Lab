from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import binascii

plaintext = b"Classified Text"

# Generate a random valid 3DES key
key = DES3.adjust_key_parity(get_random_bytes(24))
print("Key (hex):", binascii.hexlify(key).upper().decode())

cipher = DES3.new(key, DES3.MODE_ECB)
ciphertext = cipher.encrypt(pad(plaintext, DES3.block_size))
print("Ciphertext (hex):", binascii.hexlify(ciphertext).upper().decode())

decrypted = unpad(cipher.decrypt(ciphertext), DES3.block_size)
print("Decrypted text:", decrypted.decode())
