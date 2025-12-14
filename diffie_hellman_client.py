#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple

# TODO feel free to use this helper or not
UPPER_BOUND = 100
def send_common_info(sock: socket.socket) -> Tuple[int, int]:
    # TODO: Connect to the server and propose a base number and prime
    base = random.randint(1, UPPER_BOUND)
    modulus = random.randint(1, UPPER_BOUND)
    # message = "5 23"
    message = f"{base} {modulus}"
    print("Client: My proposal is ", message)
    # Send the message
    sock.sendall(message.encode('utf-8'))
    # Receive the response
    response = sock.recv(10000)
    return [base, modulus]

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_client(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_address, server_port))
        base, mod = send_common_info(s)
        client_secret = random.randint(1, UPPER_BOUND)
        client_message = base ** client_secret % mod
        print("Client: I am sending my public key", client_message)
        s.sendall(str(client_message).encode('utf-8'))
        data = s.recv(1024)
        shared_secret = int(data.decode('utf-8')) ** client_secret % mod
        print("client return", base, mod, client_secret, shared_secret)
        s.close()
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
        default=8001,
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
