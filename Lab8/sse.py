from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import json

# =============================
# 1a. Create a dataset
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
# 1b. AES Encryption/Decryption
# =============================
key = get_random_bytes(16)  # 128-bit AES key

def encrypt_AES(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return json.dumps({'iv': iv, 'ciphertext': ct})

def decrypt_AES(ciphertext_json, key):
    try:
        b64 = json.loads(ciphertext_json)
        iv = base64.b64decode(b64['iv'])
        ct = base64.b64decode(b64['ciphertext'])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')
    except Exception as e:
        print("Decryption error:", e)
        return None

# =============================
# 1c. Create an inverted index
# =============================
from collections import defaultdict

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
    encrypted_word = encrypt_AES(word, key)
    encrypted_doc_ids = [encrypt_AES(str(did), key) for did in doc_ids]
    encrypted_index[encrypted_word] = encrypted_doc_ids

# =============================
# 1d. Search Function
# =============================
def search(query, key, encrypted_index, docs):
    print(f"\n🔍 Searching for: '{query}'")

    encrypted_query = encrypt_AES(query.lower(), key)

    # Since encryption is randomized (due to random IV),
    # we can’t directly match ciphertexts.
    # So, we’ll decrypt all index terms to simulate the search.
    results = []
    for enc_word, enc_docs in encrypted_index.items():
        word = decrypt_AES(enc_word, key)
        if word == query.lower():
            for enc_doc_id in enc_docs:
                doc_id = int(decrypt_AES(enc_doc_id, key))
                results.append((doc_id, docs[doc_id]))
    if results:
        print(" Matching Documents:")
        for doc_id, text in results:
            print(f"Doc {doc_id}: {text}")
    else:
        print(" No matches found.")

# =============================
# Example Usage
# =============================
search("deep", key, encrypted_index, documents)
search("intelligence", key, encrypted_index, documents)
search("vision", key, encrypted_index, documents)
