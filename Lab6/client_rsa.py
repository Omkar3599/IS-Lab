import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

HOST = "127.0.0.1"
PORT = 65433

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("[Client] Connected to server.")

    # Receive server's public key
    server_pub_key_data = s.recv(4096)
    server_pub_key = RSA.import_key(server_pub_key_data)
    print("[Client] Received server's public key.")

    # Encrypt message
    message = "Hello, this is a secret message using RSA!"
    cipher_rsa = PKCS1_OAEP.new(server_pub_key)
    enc_message = cipher_rsa.encrypt(message.encode())

    s.sendall(enc_message)
    print("[Client] Sent encrypted message.")

    # Receive server reply
    reply = s.recv(1024).decode()
    print("[Client] Server says:", reply)

print("[Client] Done.")
