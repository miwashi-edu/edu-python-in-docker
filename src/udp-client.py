#!/usr/bin/env python3
import socket
import sys

SERVER_IP = "192.168.2.10"
SERVER_PORT = 9999
BUF = 4096
TIMEOUT_S = 3.0

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT_S)
    server = (SERVER_IP, SERVER_PORT)

    print(f"[udp-client] sending to {SERVER_IP}:{SERVER_PORT}")
    print("[udp-client] type messages; 'quit' to exit; Ctrl-C to exit")

    while True:
        try:
            line = input("> ")
        except EOFError:
            break

        if line.strip().lower() == "quit":
            break

        data = (line + "\n").encode("utf-8")
        sock.sendto(data, server)

        try:
            echo, addr = sock.recvfrom(BUF)
            print(f"[udp-client] echo from {addr[0]}:{addr[1]}: {echo.decode('utf-8', errors='replace').rstrip()}")
        except socket.timeout:
            print("[udp-client] (no response / timeout)")

    sock.close()
    print("[udp-client] bye")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[udp-client] bye")
        sys.exit(0)

