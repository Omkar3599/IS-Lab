import socket
import hashlib
import threading
import time

HOST = '127.0.0.1'
PORT = 65432

def compute_hash(data):
    sha = hashlib.sha256()
    sha.update(data)
    return sha.digest()

# Server code running in a thread
def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        with conn:
            print('Server connected by', addr)
            data = conn.recv(1024)
            if not data:
                print("Server received no data")
            else:
                print(f"Server received data: {data}")

                # Compute hash of received data
                data_hash = compute_hash(data)

                # Send hash back to client
                conn.sendall(data_hash)
                print(f"Server sent hash: {data_hash.hex()}")

# Client code to send data and verify hash
def client(data_to_send):
    time.sleep(1)  # wait a bit to let server start
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Client sending data: {data_to_send}")
        s.sendall(data_to_send)

        # Receive hash from server
        data_hash = s.recv(1024)
        print(f"Client received hash: {data_hash.hex()}")

        # Verify integrity
        local_hash = compute_hash(data_to_send)
        if local_hash == data_hash:
            print("Integrity check PASSED: Data is intact.")
        else:
            print("Integrity check FAILED: Data corrupted or tampered!")

if __name__ == "__main__":
    # Start server in a separate thread
    server_thread = threading.Thread(target=server, daemon=True)
    server_thread.start()

    # Example data to send
    data = b"Hello, secure world!"

    # Uncomment this line to simulate tampering and see failure:
    # data = b"Hello, insecure world!"

    # Run client code
    client(data)

    # Wait for server thread to finish (optional)
    server_thread.join(timeout=2)
