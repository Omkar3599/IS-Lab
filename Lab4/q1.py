import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# -------------------------
# Diffie-Hellman Key Exchange
# -------------------------
def diffie_hellman():
    p = 23  # prime
    g = 5   # primitive root
    a = random.randint(1, p-1)  # private key for peer A
    b = random.randint(1, p-1)  # private key for peer B
    A = pow(g, a, p)            # public key A
    B = pow(g, b, p)            # public key B
    secret_A = pow(B, a, p)     # shared secret for A
    secret_B = pow(A, b, p)     # shared secret for B
    return secret_A, secret_B

# -------------------------
# RSA Key Management
# -------------------------
class KeyManager:
    def __init__(self):
        self.keys = {}

    def generate_rsa_keys(self, system_name):
        key = RSA.generate(2048)
        private_key = key
        public_key = key.publickey()
        self.keys[system_name] = {"private": private_key, "public": public_key}
        return public_key, private_key

    def revoke_key(self, system_name):
        if system_name in self.keys:
            del self.keys[system_name]

# -------------------------
# RSA Encryption/Decryption
# -------------------------
def rsa_encrypt(message, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(message.encode())

def rsa_decrypt(ciphertext, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(ciphertext).decode()

# -------------------------
# Demo for SecureCorp
# -------------------------
if __name__ == "__main__":
    print("=== SecureCorp Communication System ===")

    # Key Manager
    km = KeyManager()

    # Generate RSA keys for 3 systems
    pubA, privA = km.generate_rsa_keys("Finance")
    pubB, privB = km.generate_rsa_keys("HR")
    pubC, privC = km.generate_rsa_keys("SupplyChain")

    print("\n--- Diffie-Hellman Shared Secret ---")
    sA, sB = diffie_hellman()
    print(f"Shared Secret A: {sA}, Shared Secret B: {sB}")

    print("\n--- RSA Secure Messaging ---")
    msg = "Financial Report Q3"
    encrypted = rsa_encrypt(msg, pubB)   # Finance -> HR
    print("Encrypted (Finance -> HR):", encrypted[:50], "...")

    decrypted = rsa_decrypt(encrypted, privB)
    print("HR Decrypted:", decrypted)

    # Revoke HR key
    km.revoke_key("HR")
    print("\nHR key revoked. Remaining keys:", list(km.keys.keys()))
