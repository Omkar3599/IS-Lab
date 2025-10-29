import socket
import hmac
import hashlib

HOST = '127.0.0.1'
PORT = 65433
SECRET_KEY = b'shared_secret_key'

def compute_hmac(data):
    return hmac.new(SECRET_KEY, data, hashlib.sha256).digest()

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[Server] Listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        with conn:
            print(f"[Server] Connected by {addr}")
            packet = conn.recv(2048)
            if not packet:
                return

            # Split data and received hmac
            message, received_hmac = packet[:-32], packet[-32:]
            computed_hmac = compute_hmac(message)

            print(f"[Server] Message received: {message.decode()}")
            print(f"[Server] Received HMAC: {received_hmac.hex()}")
            print(f"[Server] Computed HMAC: {computed_hmac.hex()}")

            if hmac.compare_digest(received_hmac, computed_hmac):
                conn.sendall(b"Integrity and authenticity verified ")
            else:
                conn.sendall(b"Verification failed ")

if __name__ == "__main__":
    server()
