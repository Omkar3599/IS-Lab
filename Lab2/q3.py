import time
import binascii
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad

# Test message
message = b"Performance Testing of Encryption Algorithms"

# --- DES Setup ---
des_key = b"8bytekey"        # DES requires 8-byte key
des_cipher = DES.new(des_key, DES.MODE_ECB)

# --- AES-256 Setup ---
aes_key = b"0123456789ABCDEF0123456789ABCDEF"  # 32-byte key (256 bits)
aes_cipher = AES.new(aes_key, AES.MODE_ECB)

# --- DES Timing ---
start = time.time()
des_encrypted = des_cipher.encrypt(pad(message, DES.block_size))
des_encrypt_time = time.time() - start

start = time.time()
des_decrypted = unpad(des_cipher.decrypt(des_encrypted), DES.block_size)
des_decrypt_time = time.time() - start

# --- AES-256 Timing ---
start = time.time()
aes_encrypted = aes_cipher.encrypt(pad(message, AES.block_size))
aes_encrypt_time = time.time() - start

start = time.time()
aes_decrypted = unpad(aes_cipher.decrypt(aes_encrypted), AES.block_size)
aes_decrypt_time = time.time() - start

# --- Results ---
print("DES Encryption Time:   {:.6f} sec".format(des_encrypt_time))
print("DES Decryption Time:   {:.6f} sec".format(des_decrypt_time))
print("AES-256 Encryption Time: {:.6f} sec".format(aes_encrypt_time))
print("AES-256 Decryption Time: {:.6f} sec".format(aes_decrypt_time))

print("\nDES Decrypted Message: ", des_decrypted.decode())
print("AES Decrypted Message: ", aes_decrypted.decode())
