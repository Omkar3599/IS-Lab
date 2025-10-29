import random

# Generate a large prime number for modulus p and a primitive root g
# For simplicity, we'll use small safe prime p and g

p = 0xFFFFFFFB  # a large prime (for demo, not cryptographically secure)
g = 5  # primitive root mod p (assumed)


# Function to generate private key (random int)
def generate_private_key(p):
    return random.randint(2, p - 2)


# Compute public key = g^private_key mod p
def generate_public_key(private_key, p, g):
    return pow(g, private_key, p)


# Compute shared secret = other_party_public_key ^ private_key mod p
def compute_shared_secret(other_public, private_key, p):
    return pow(other_public, private_key, p)


# Simulate DH key exchange
def diffie_hellman_demo():
    print("Diffie-Hellman Key Exchange Demo\n")

    # Alice generates private and public keys
    alice_private = generate_private_key(p)
    alice_public = generate_public_key(alice_private, p, g)
    print(f"Alice's Private Key: {alice_private}")
    print(f"Alice's Public Key: {alice_public}\n")

    # Bob generates private and public keys
    bob_private = generate_private_key(p)
    bob_public = generate_public_key(bob_private, p, g)
    print(f"Bob's Private Key: {bob_private}")
    print(f"Bob's Public Key: {bob_public}\n")

    # Alice computes shared secret using Bob's public key
    alice_shared_secret = compute_shared_secret(bob_public, alice_private, p)
    # Bob computes shared secret using Alice's public key
    bob_shared_secret = compute_shared_secret(alice_public, bob_private, p)

    print(f"Alice's computed shared secret: {alice_shared_secret}")
    print(f"Bob's computed shared secret: {bob_shared_secret}")

    if alice_shared_secret == bob_shared_secret:
        print("\nShared secret matches! Key exchange successful.")
    else:
        print("\nShared secret mismatch! Key exchange failed.")


if __name__ == "__main__":
    diffie_hellman_demo()
