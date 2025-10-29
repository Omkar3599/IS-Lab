from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# Generate ECC keys
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Message
message = b"Secure Transactions"

# Encrypt
ephemeral_private_key = ec.generate_private_key(ec.SECP256R1())
shared_key = ephemeral_private_key.exchange(ec.ECDH(), public_key)

# Derive AES key from shared secret
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data'
).derive(shared_key)

aesgcm = AESGCM(derived_key)
nonce = os.urandom(12)
ciphertext = aesgcm.encrypt(nonce, message, None)

# Transmit: (ephemeral public key, nonce, ciphertext)
ephemeral_public_key = ephemeral_private_key.public_key()

# ---- Decryption ----
shared_key2 = private_key.exchange(ec.ECDH(), ephemeral_public_key)
derived_key2 = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data'
).derive(shared_key2)

aesgcm2 = AESGCM(derived_key2)
plaintext = aesgcm2.decrypt(nonce, ciphertext, None)

print("Original:", message.decode())
print("Ciphertext:", ciphertext)
print("Decrypted:", plaintext.decode())
