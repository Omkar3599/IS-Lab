import socket
import hmac
import hashlib

HOST = '127.0.0.1'
PORT = 65433
SECRET_KEY = b'shared_secret_key'

def compute_hmac(data):
    return hmac.new(SECRET_KEY, data, hashlib.sha256).digest()

def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        message = b"Confidential data: patient record 12345"
        hmac_tag = compute_hmac(message)
        packet = message + hmac_tag

        print(f"[Client] Sending message: {message.decode()}")
        print(f"[Client] HMAC: {hmac_tag.hex()}")

        s.sendall(packet)
        response = s.recv(1024).decode()
        print("[Client] Server response:", response)

if __name__ == "__main__":
    client()
