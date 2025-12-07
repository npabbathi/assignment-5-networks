#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple

# TODO feel free to use this helper or not
def send_common_info(sock: socket.socket, server_address: str, server_port: int) -> Tuple[int, int]:
    # TODO: Connect to the server and propose a base number and prime
    try:
        # Create a socket object
            # Connect to the server
            sock.connect((server_address, server_port))
            message = "5 23"
            # Send the message
            sock.sendall(message.encode('utf-8'))
            # Receive the response
            response = sock.recv(10000)
            
            return [5, 23]
    except Exception as e:
        return f"An error occurred: {e}"
    # TODO: You can generate these randomly, or just use a fixed set
    # TODO: Return the tuple (base, prime modulus)
    pass

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_client(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    # TODO: Create a socket 
    # TODO: Send the proposed base and modulus number to the server using send_common_info
    base, mod = send_common_info(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_address, server_port)

    # TODO: Come up with a random secret key
    client_secret = random.randint(1, 100)

    # TODO: Calculate the message the client sends using the secret integer.
    client_message = base ** client_secret % mod
    # TODO: Exchange messages with the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_address, server_port))
        s.sendall(str(client_message).encode('utf-8'))
        data = s.recv(1024)
    # TODO: Calculate the secret using your own secret key and server message
    shared_secret = data.decode('utf-8') ** client_secret % mod
    # TODO: Return the base number, the modulus, the private key, and the shared secret
    print("client return", base, mod, client_secret, shared_secret)
    return (base, mod, client_secret, shared_secret)



def main(args):
    if args.seed:
        random.seed(args.seed)
    
    dh_exchange_client(args.address, args.port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the client will connect to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the client will connect to.",
    )
    parser.add_argument(
        "--seed",
        dest="seed",
        type=int,
        help="Random seed to make the exchange deterministic.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
