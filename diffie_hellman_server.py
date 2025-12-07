#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple

# TODO feel free to use this helper or not
def receive_common_info(server_address: str, server_port: int) -> Tuple[int, int]:
    # TODO: Wait for a client message that sends a base number.

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server_address, server_port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
                data = data.decode('utf-8')
                a, b = map(int, data.split())
    s.close()
    return (a, b)
    # TODO: Return the tuple (base, prime modulus)
        

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_server(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    # TODO: Create a server socket. can be UDP or TCP.
    # TODO: Read client's proposal for base and modulus using receive_common_info
    base, modulus = receive_common_info(server_address, server_port)

    # TODO: Generate your own secret key
    server_secret = random.randint(1, 100)
    # TODO: Exchange messages with the client
    server_message = base ** server_secret % modulus
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server_address, server_port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(str(server_message).encode('utf-8'))

    # TODO: Compute the shared secret.
    shared_secret = data.decode('utf-8') ** server_secret % modulus

    # TODO: Return the base number, prime modulus, the secret integer, and the shared secret
    print("server return", base, modulus, server_secret, shared_secret)
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
