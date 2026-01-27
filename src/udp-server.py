#!/usr/bin/env python3
import socket

HOST = "0.0.0.0"
PORT = 9999
BUF = 4096

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[udp-server] listening on {HOST}:{PORT}")

    while True:
        data, addr = sock.recvfrom(BUF)
        if not data:
            continue
        msg = data.decode("utf-8", errors="replace")
        print(f"[udp-server] from {addr[0]}:{addr[1]}: {msg}")

        # echo back exactly what we got
        sock.sendto(data, addr)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[udp-server] bye")

