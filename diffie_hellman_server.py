#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple

# TODO feel free to use this helper or not
def receive_common_info(conn: socket.socket) -> Tuple[int, int]:
    # TODO: Wait for a client message that sends a base number.
    data = conn.recv(1024)
    conn.sendall(data)
    data = data.decode('utf-8')
    a, b = map(int, data.split())
    print("Server: I got the proposal", data)
    return (a, b)
    # TODO: Return the tuple (base, prime modulus)
        

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_server(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server_address, server_port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            base, modulus = receive_common_info(conn)
            server_secret = random.randint(1, 100)
            server_message = base ** server_secret % modulus
            print("Server: I am sending my public key", secret_message)
            conn.sendall(str(server_message).encode('utf-8'))

            data = conn.recv(1024)

    shared_secret = int(data.decode('utf-8')) ** server_secret % modulus
    print("server return", base, modulus, server_secret, shared_secret)
    s.close()
    return (base, modulus, server_secret, shared_secret)

def main(args):
    dh_exchange_server(args.address, args.port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the server will bind to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the server will listen on.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
