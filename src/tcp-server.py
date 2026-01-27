#!/usr/bin/env python3
import socket
import threading

HOST = "0.0.0.0"
PORT = 9998
BUF = 4096

def handle_client(conn, addr):
    print(f"[tcp-server] client connected {addr[0]}:{addr[1]}")
    try:
        with conn:
            while True:
                data = conn.recv(BUF)
                if not data:
                    break
                msg = data.decode("utf-8", errors="replace").rstrip("\n")
                print(f"[tcp-server] from {addr[0]}:{addr[1]}: {msg}")
                conn.sendall(data)  # echo
    finally:
        print(f"[tcp-server] client disconnected {addr[0]}:{addr[1]}")

def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(16)
    print(f"[tcp-server] listening on {HOST}:{PORT}")

    while True:
        conn, addr = srv.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[tcp-server] bye")

