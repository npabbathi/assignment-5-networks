import socket
import threading
import time

def crack_shared_secret(base, modulus, client_pub, server_pub):
    """
    Attempts to crack the shared secret by brute-forcing the discrete logarithm.
    Assumes small modulus for feasibility.
    """
    # Find client_secret such that base ** client_secret % modulus == client_pub
    for client_secret in range(1, modulus):
        if pow(base, client_secret, modulus) == client_pub:
            # Now compute shared_secret = server_pub ** client_secret % modulus
            shared_secret = pow(server_pub, client_secret, modulus)
            return shared_secret
    return None  # If not found, though with small mod it should be

def handle_client(client_socket, remote_host, remote_port):
    # Connect to remote server
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    messages = []

    def forward(src, dst, direction):
        while True:
            try:
                data = src.recv(1024)
                if not data:
                    break
                messages.append((direction, data.decode('utf-8', errors='ignore')))
                dst.sendall(data)
            except:
                break

    # Start threads to forward data
    threading.Thread(target=forward, args=(client_socket, remote_socket, "client_to_server")).start()
    threading.Thread(target=forward, args=(remote_socket, client_socket, "server_to_client")).start()

    # Wait a bit for exchange to complete
    time.sleep(2)

    # Parse messages
    base = modulus = client_pub = server_pub = None
    for direction, msg in messages:
        if direction == "client_to_server" and not base:
            parts = msg.strip().split()
            if len(parts) == 2:
                base, modulus = map(int, parts)
        elif direction == "server_to_client" and base and not client_pub:
            # Server echoes base mod, then sends its pub
            if msg.strip() == f"{base} {modulus}":
                continue
            try:
                server_pub = int(msg.strip())
            except:
                pass
        elif direction == "client_to_server" and base and server_pub and not client_pub:
            try:
                client_pub = int(msg.strip())
            except:
                pass

    start_time = time.perf_counter()
    if base and modulus and client_pub and server_pub:
        shared = crack_shared_secret(base, modulus, client_pub, server_pub)
        if shared is not None:
            end_time = time.perf_counter()
            print("Cracking completed in:", end_time - start_time)
            print(f"Cracked shared secret: {shared}")
        else:
            print("Failed to crack shared secret")
    else:
        print("Could not extract necessary values from packets")

def proxy_server(local_port, remote_host, remote_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', local_port))
    server.listen(5)
    print(f"Proxy listening on port {local_port}, forwarding to {remote_host}:{remote_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port)).start()

if __name__ == "__main__":
    # Run the proxy server
    proxy_server(8001, "127.0.0.1", 8000)
