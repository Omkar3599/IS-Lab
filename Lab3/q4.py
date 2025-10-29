# simple_filetransfer_bench_windows.py
# Simple benchmark: RSA-2048 vs ECC (secp256r1) hybrid file encryption (AES-256-GCM)
# Windows-friendly (no shebang). Requires: pip install cryptography

import time
import secrets
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

# ---------- helpers ----------
def now(): return time.perf_counter()

def write_bytes(path: Path, data: bytes):
    path.write_bytes(data)

def read_bytes(path: Path) -> bytes:
    return path.read_bytes()

def make_random_file(path: Path, size_bytes: int):
    if path.exists() and path.stat().st_size == size_bytes:
        print(f"{path.name} already exists.")
        return
    print(f"Creating {path.name} ({size_bytes//1024} KB)...")
    chunk = 64 * 1024
    with open(path, "wb") as f:
        written = 0
        while written < size_bytes:
            towrite = min(chunk, size_bytes - written)
            f.write(secrets.token_bytes(towrite))
            written += towrite

# ---------- key generation ----------
def gen_rsa_2048():
    t0 = now()
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    t1 = now()
    return priv, t1 - t0

def gen_ec_secp256r1():
    t0 = now()
    priv = ec.generate_private_key(ec.SECP256R1(), default_backend())
    t1 = now()
    return priv, t1 - t0

# ---------- RSA-hybrid (RSA-OAEP + AES-GCM) ----------
def rsa_hybrid_encrypt(pubkey, infile: Path, outfile: Path):
    data = read_bytes(infile)
    aes_key = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(aes_key)
    nonce = secrets.token_bytes(12)

    t0 = now()
    ciphertext = aesgcm.encrypt(nonce, data, None)   # includes tag
    t1 = now(); enc_time = t1 - t0

    rsa_encrypted_key = pubkey.encrypt(
        aes_key,
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    out = len(rsa_encrypted_key).to_bytes(2, "big") + rsa_encrypted_key + nonce + ciphertext
    write_bytes(outfile, out)
    return enc_time, len(out), len(rsa_encrypted_key)

def rsa_hybrid_decrypt(privkey, infile: Path, outfile: Path):
    b = read_bytes(infile)
    keylen = int.from_bytes(b[:2], "big")
    pos = 2
    rsa_enc_key = b[pos:pos+keylen]; pos += keylen
    nonce = b[pos:pos+12]; pos += 12
    ciphertext = b[pos:]

    t0 = now()
    aes_key = privkey.decrypt(
        rsa_enc_key,
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    t1 = now(); dec_time = t1 - t0

    write_bytes(outfile, plaintext)
    return dec_time, len(plaintext)

# ---------- ECIES-like hybrid (ECDH ephemeral + HKDF -> AES-GCM) ----------
def ecies_encrypt(pubkey, infile: Path, outfile: Path):
    data = read_bytes(infile)
    eph_priv = ec.generate_private_key(ec.SECP256R1(), default_backend())
    eph_pub = eph_priv.public_key()
    eph_pem = eph_pub.public_bytes(encoding=serialization.Encoding.PEM,
                                   format=serialization.PublicFormat.SubjectPublicKeyInfo)

    shared = eph_priv.exchange(ec.ECDH(), pubkey)
    aes_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'file-transfer').derive(shared)
    aesgcm = AESGCM(aes_key)
    nonce = secrets.token_bytes(12)

    t0 = now()
    ciphertext = aesgcm.encrypt(nonce, data, None)
    t1 = now(); enc_time = t1 - t0

    out = len(eph_pem).to_bytes(2, "big") + eph_pem + nonce + ciphertext
    write_bytes(outfile, out)
    return enc_time, len(out), len(eph_pem)

def ecies_decrypt(privkey, infile: Path, outfile: Path):
    b = read_bytes(infile)
    plen = int.from_bytes(b[:2], "big")
    pos = 2
    eph_pem = b[pos:pos+plen]; pos += plen
    nonce = b[pos:pos+12]; pos += 12
    ciphertext = b[pos:]

    eph_pub = serialization.load_pem_public_key(eph_pem, backend=default_backend())
    shared = privkey.exchange(ec.ECDH(), eph_pub)
    aes_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'file-transfer').derive(shared)
    aesgcm = AESGCM(aes_key)

    t0 = now()
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    t1 = now(); dec_time = t1 - t0

    write_bytes(outfile, plaintext)
    return dec_time, len(plaintext)

# ---------- run benchmark ----------
def run():
    # prepare files
    f1 = Path("test_1MB.bin")
    f2 = Path("test_10MB.bin")
    make_random_file(f1, 1 * 1024 * 1024)
    make_random_file(f2, 10 * 1024 * 1024)
    files = [f1, f2]

    # keys
    rsa_priv, rsa_t = gen_rsa_2048()
    rsa_pub = rsa_priv.public_key()
    ec_priv, ec_t = gen_ec_secp256r1()
    ec_pub = ec_priv.public_key()

    print(f"Keygen times: RSA-2048 = {rsa_t:.4f}s, EC-secp256r1 = {ec_t:.4f}s\n")

    results = []
    for f in files:
        size_mb = f.stat().st_size / (1024*1024)
        print(f"--- File: {f.name} ({size_mb:.2f} MB) ---")

        # RSA hybrid
        rsa_ct = f.with_suffix(".rsa.ct")
        rsa_dec = f.with_suffix(".rsa.dec")
        enc_t, ct_sz, rsa_key_overhead = rsa_hybrid_encrypt(rsa_pub, f, rsa_ct)
        dec_t, dec_sz = rsa_hybrid_decrypt(rsa_priv, rsa_ct, rsa_dec)
        ok = read_bytes(rsa_dec) == read_bytes(f)
        print(f"RSA: enc {enc_t:.4f}s, dec {dec_t:.4f}s, ok={ok}, ct_bytes={ct_sz}, key_overhead={rsa_key_overhead}")

        # ECIES hybrid
        ec_ct = f.with_suffix(".ec.ct")
        ec_dec = f.with_suffix(".ec.dec")
        enc_t2, ct_sz2, ec_overhead = ecies_encrypt(ec_pub, f, ec_ct)
        dec_t2, dec_sz2 = ecies_decrypt(ec_priv, ec_ct, ec_dec)
        ok2 = read_bytes(ec_dec) == read_bytes(f)
        print(f"ECC: enc {enc_t2:.4f}s, dec {dec_t2:.4f}s, ok={ok2}, ct_bytes={ct_sz2}, eph_overhead={ec_overhead}\n")

        results.append({
            "file": f.name,
            "size_MB": size_mb,
            "rsa_enc_s": enc_t, "rsa_dec_s": dec_t,
            "rsa_ct_bytes": ct_sz, "rsa_keyover": rsa_key_overhead, "rsa_ok": ok,
            "ec_enc_s": enc_t2, "ec_dec_s": dec_t2,
            "ec_ct_bytes": ct_sz2, "ec_overhead": ec_overhead, "ec_ok": ok2
        })

    print("Summary results:")
    for r in results:
        print(r)

if __name__ == "__main__":
    run()
