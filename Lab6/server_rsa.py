import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate RSA key pair (server)
server_key = RSA.generate(2048)
private_key = server_key
public_key = server_key.publickey()

HOST = "127.0.0.1"
PORT = 65433

print("[Server] Starting on port", PORT)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print(f"[Server] Connection from {addr}")

    # Send public key to client
    conn.sendall(public_key.export_key())

    # Receive encrypted data
    enc_data = conn.recv(4096)

    # Decrypt message
    cipher_rsa = PKCS1_OAEP.new(private_key)
    message = cipher_rsa.decrypt(enc_data).decode()
    print("[Server] Decrypted message:", message)

    # Send acknowledgment
    reply = f"Received your message securely: {message[:15]}..."
    conn.sendall(reply.encode())

print("[Server] Done.")
