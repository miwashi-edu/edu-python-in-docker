#!/usr/bin/env python3
import socket
import sys

SERVER_IP = "192.168.2.10"
SERVER_PORT = 9998
BUF = 4096

def recv_line(sock: socket.socket) -> bytes:
    # read until newline to mirror the client's newline-delimited sends
    chunks = []
    while True:
        b = sock.recv(1)
        if not b:
            return b""
        chunks.append(b)
        if b == b"\n":
            return b"".join(chunks)

def main():
    print(f"[tcp-client] connecting to {SERVER_IP}:{SERVER_PORT}")
    with socket.create_connection((SERVER_IP, SERVER_PORT)) as sock:
        print("[tcp-client] connected")
        print("[tcp-client] type messages; 'quit' to exit; Ctrl-C to exit")

        while True:
            try:
                line = input("> ")
            except EOFError:
                break

            if line.strip().lower() == "quit":
                break

            sock.sendall((line + "\n").encode("utf-8"))

            echo = recv_line(sock)
            if not echo:
                print("[tcp-client] server closed connection")
                break
            print(f"[tcp-client] echo: {echo.decode('utf-8', errors='replace').rstrip()}")

    print("[tcp-client] bye")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[tcp-client] bye")
        sys.exit(0)

