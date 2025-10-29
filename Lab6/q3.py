import socket
import random
import threading
import time
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Diffie-Hellman params (small prime for demo only)
p = 0xFFFFFFFB
g = 5

def derive_aes_key(shared_secret):
    key_bytes = shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8, 'big')
    return hashlib.sha256(key_bytes).digest()[:16]  # AES-128 key

def aes_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ct_bytes

def aes_decrypt(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return pt.decode()

def generate_private_key(p):
    return random.randint(2, p - 2)

def generate_public_key(private_key, p, g):
    return pow(g, private_key, p)

def compute_shared_secret(other_public, private_key, p):
    return pow(other_public, private_key, p)

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(1)
    print("[Server] Listening on port 65432...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"[Server] Connected by {addr}")

        server_private = generate_private_key(p)
        server_public = generate_public_key(server_private, p, g)

        # Receive client public key
        client_public_bytes = conn.recv(1024)
        client_public = int.from_bytes(client_public_bytes, 'big')
        print(f"[Server] Received client public key: {client_public}")

        # Send server public key
        conn.sendall(server_public.to_bytes((server_public.bit_length() + 7) // 8, 'big'))
        print(f"[Server] Sent server public key: {server_public}")

        shared_secret = compute_shared_secret(client_public, server_private, p)
        print(f"[Server] Shared secret computed: {shared_secret}")

        aes_key = derive_aes_key(shared_secret)

        # Receive encrypted message
        encrypted_message = conn.recv(1024)
        print(f"[Server] Encrypted message received: {encrypted_message.hex()}")

        # Decrypt message
        message = aes_decrypt(aes_key, encrypted_message)
        print(f"[Server] Decrypted message: {message}")

        # Send encrypted acknowledgment
        response = "Message received loud and clear."
        encrypted_response = aes_encrypt(aes_key, response)
        conn.sendall(encrypted_response)
        print("[Server] Sent encrypted acknowledgment.")

def client():
    time.sleep(1)  # Ensure server is listening before client connects
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))

    client_private = generate_private_key(p)
    client_public = generate_public_key(client_private, p, g)

    # Send client public key
    client_socket.sendall(client_public.to_bytes((client_public.bit_length() + 7) // 8, 'big'))
    print(f"[Client] Sent client public key: {client_public}")

    # Receive server public key
    server_public_bytes = client_socket.recv(1024)
    server_public = int.from_bytes(server_public_bytes, 'big')
    print(f"[Client] Received server public key: {server_public}")

    shared_secret = compute_shared_secret(server_public, client_private, p)
    print(f"[Client] Shared secret computed: {shared_secret}")

    aes_key = derive_aes_key(shared_secret)

    # Encrypt and send message
    message = "Hello, this is a secret message from client."
    encrypted_message = aes_encrypt(aes_key, message)
    client_socket.sendall(encrypted_message)
    print(f"[Client] Sent encrypted message: {encrypted_message.hex()}")

    # Receive encrypted acknowledgment
    encrypted_response = client_socket.recv(1024)
    response = aes_decrypt(aes_key, encrypted_response)
    print(f"[Client] Decrypted acknowledgment from server: {response}")

    client_socket.close()

if __name__ == "__main__":
    server_thread = threading.Thread(target=server, daemon=True)
    client_thread = threading.Thread(target=client, daemon=True)

    server_thread.start()
    client_thread.start()

    server_thread.join()
    client_thread.join()
