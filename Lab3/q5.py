import random
import time

# A 2048-bit safe prime (RFC 3526 Group 14)
p = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A63A36210000000000090563", 16
)

g = 2  # generator (commonly 2 for DH)

def generate_private_key(p):
    # Private key: random number < p
    return random.randint(2, p - 2)

def generate_public_key(private_key, g, p):
    return pow(g, private_key, p)

def compute_shared_secret(peer_public, private_key, p):
    return pow(peer_public, private_key, p)

# ---- Simulation ----
start_time = time.time()

# Peer A
a_private = generate_private_key(p)
a_public = generate_public_key(a_private, g, p)

# Peer B
b_private = generate_private_key(p)
b_public = generate_public_key(b_private, g, p)

# Exchange public keys and compute shared secret
shared_secret_A = compute_shared_secret(b_public, a_private, p)
shared_secret_B = compute_shared_secret(a_public, b_private, p)

end_time = time.time()

print("Prime size (bits):", p.bit_length())
print("Peer A Public (first 50 digits):", str(a_public)[:50], "...")
print("Peer B Public (first 50 digits):", str(b_public)[:50], "...")
print("Shared Secret Match?", shared_secret_A == shared_secret_B)
print("Time taken: {:.6f} seconds".format(end_time - start_time))
