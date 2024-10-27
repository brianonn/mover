#!/usr/bin/env python3

import os
import socket
import sys

# Define server host and port
HOST = 'localhost'  # Change to the server's IP address if remote
PORT = 5000         # Port the server is listening on

def send_file(filename, sock):
    # Send the filename as the first line
    sock.sendall(f"{filename}\n".encode())

    # Send the contents of the file
    with open(filename, 'r') as file:
        for line in file:
            sock.sendall(line.encode())

    # Send the termination line
    sock.sendall("ENDENDEND\n".encode())
    print(f"Sent file: {filename}")

def main():
    # Check if any filenames were provided as command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python send_client.py <filename1> <filename2> ...")
        sys.exit(1)

    # Iterate over each filename given as a command-line argument
    for filename in sys.argv[1:]:
        if os.path.isfile(filename):
            # Create a TCP socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to the server
                sock.connect((HOST, PORT))
                send_file(filename, sock)
        else:
            print(f"File not found: {filename}")

if __name__ == "__main__":
    main()
