import random
import time
import logging
from datetime import datetime, timedelta

# ---------------- Logging Setup ----------------
logging.basicConfig(filename="key_mgmt.log", level=logging.INFO, format="%(asctime)s - %(message)s")
logging.getLogger().addHandler(logging.StreamHandler())  # also show logs on console

# ---------------- Fast Prime Test (Miller-Rabin) ----------------
def is_prime(n, k=10):  # k = number of rounds
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(bits=512):
    """Generate a prime of given bit size"""
    while True:
        candidate = random.getrandbits(bits) | 1 | (1 << (bits - 1))
        if is_prime(candidate):
            return candidate

# ---------------- Rabin Key Pair ----------------
def rabin_keygen(bits=1024):
    p = generate_large_prime(bits // 2)
    q = generate_large_prime(bits // 2)
    n = p * q
    return {"public": n, "private": (p, q)}

# ---------------- Key Management Service ----------------
class KeyManagementService:
    def __init__(self):
        self.keys = {}
        self.expiry = {}

    def generate_keys(self, system_id, bits=1024):
        keypair = rabin_keygen(bits)
        self.keys[system_id] = keypair
        self.expiry[system_id] = datetime.now() + timedelta(days=365)
        logging.info(f"[GEN] Keys generated for {system_id}")
        return keypair

    def distribute_keys(self, system_id):
        if system_id in self.keys:
            logging.info(f"[DIST] Keys distributed to {system_id}")
            return self.keys[system_id]
        else:
            logging.warning(f"[DIST] No keys for {system_id}")
            return None

    def revoke_keys(self, system_id):
        if system_id in self.keys:
            del self.keys[system_id]
            del self.expiry[system_id]
            logging.info(f"[REVOKE] Keys revoked for {system_id}")

    def renew_keys(self, system_id, bits=1024):
        if system_id in self.keys:
            self.keys[system_id] = rabin_keygen(bits)
            self.expiry[system_id] = datetime.now() + timedelta(days=365)
            logging.info(f"[RENEW] Keys renewed for {system_id}")

# ---------------- Demo ----------------
if __name__ == "__main__":
    kms = KeyManagementService()

    # Generate keys for hospitals/clinics
    kms.generate_keys("Hospital_A", bits=512)   # smaller for speed
    kms.generate_keys("Clinic_B", bits=512)

    # Distribute
    kms.distribute_keys("Hospital_A")
    kms.distribute_keys("Clinic_B")

    # Renewal
    kms.renew_keys("Hospital_A")

    # Revocation
    kms.revoke_keys("Clinic_B")

    logging.info("Key Management Demo Completed")
