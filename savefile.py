#!/usr/bin/env python3

import socket
import sys

# Define default host and port
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 5000      # Port to listen on (non-privileged ports > 1023)

def start_server(host,port):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Listening on {HOST}:{PORT}")

        while True:
            # Wait for a connection
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            with conn:
                handle_client(conn)

def handle_client(conn):
    with conn.makefile('r') as client_file:
        filename = None
        file = None

        for line in client_file:
            if filename is None:
                # The first line should be the filename
                filename = line.strip()
                file = open(filename, 'w')
                print(f"Writing to file: {filename}")
            elif line.strip() == "ENDENDEND":
                # Close the file and reset state
                if file:
                    file.close()
                    print(f"Closed file: {filename}")
                break  # end the current client
            else:
                # Write line to the file
                if file:
                    file.write(line)

if __name__ == "__main__":

    # Check if host:port was provided as an argument
    if len(sys.argv) > 2:
        print("Usage: python server_script.py [host:port]")
        sys.exit(1)

    if len(sys.argv) == 2:
        # Parse host and port from the first argument
        host_port = sys.argv[1].split(":")
        HOST = host_port[0]
        PORT = int(host_port[1])

    start_server(HOST,PORT)
