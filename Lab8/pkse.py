from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from collections import defaultdict
import base64

# =============================
# 2a. Create a dataset
# =============================
documents = {
    1: "Machine learning enables computers to learn from data",
    2: "Deep learning is a subset of machine learning",
    3: "Natural language processing is part of artificial intelligence",
    4: "Neural networks are used in deep learning",
    5: "Data science involves statistics and machine learning",
    6: "Artificial intelligence powers modern applications",
    7: "Computer vision is a field of artificial intelligence",
    8: "Supervised learning uses labeled data",
    9: "Unsupervised learning finds hidden patterns in data",
    10: "Reinforcement learning trains agents through rewards"
}

# =============================
# 2b. RSA Encryption/Decryption
# =============================
key_pair = RSA.generate(2048)
public_key = key_pair.publickey()
encryptor = PKCS1_OAEP.new(public_key)
decryptor = PKCS1_OAEP.new(key_pair)

def encrypt_RSA(plaintext: str) -> str:
    """Encrypt text using RSA public key."""
    ciphertext = encryptor.encrypt(plaintext.encode('utf-8'))
    return base64.b64encode(ciphertext).decode('utf-8')

def decrypt_RSA(ciphertext: str) -> str:
    """Decrypt text using RSA private key."""
    decoded = base64.b64decode(ciphertext)
    plaintext = decryptor.decrypt(decoded)
    return plaintext.decode('utf-8')

# =============================
# 2c. Create Encrypted Inverted Index
# =============================
def build_inverted_index(docs):
    index = defaultdict(set)
    for doc_id, text in docs.items():
        for word in text.lower().split():
            index[word].add(doc_id)
    return index

inverted_index = build_inverted_index(documents)

# Encrypt the inverted index
encrypted_index = {}
for word, doc_ids in inverted_index.items():
    encrypted_word = encrypt_RSA(word)
    encrypted_doc_ids = [encrypt_RSA(str(did)) for did in doc_ids]
    encrypted_index[encrypted_word] = encrypted_doc_ids

# =============================
# 2d. Search Function
# =============================
def search(query, encrypted_index, docs):
    print(f"\n🔍 Searching for: '{query}'")

    encrypted_query = encrypt_RSA(query.lower())

    # Because RSA encryption uses random padding (non-deterministic),
    # ciphertexts differ even for the same plaintext.
    # To simulate search, we decrypt the index words for matching.
    results = []
    for enc_word, enc_doc_ids in encrypted_index.items():
        word = decrypt_RSA(enc_word)
        if word == query.lower():
            for enc_doc_id in enc_doc_ids:
                doc_id = int(decrypt_RSA(enc_doc_id))
                results.append((doc_id, docs[doc_id]))

    if results:
        print("✅ Matching Documents:")
        for doc_id, text in results:
            print(f"Doc {doc_id}: {text}")
    else:
        print("❌ No matches found.")

# =============================
# Example Usage
# =============================
search("learning", encrypted_index, documents)
search("intelligence", encrypted_index, documents)
search("vision", encrypted_index, documents)
