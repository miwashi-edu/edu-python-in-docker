import socket

HOST = "192.168.2.10"
PORT = 5000

msg = "hello over tcp\n"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(msg.encode("utf-8"))
    reply = s.recv(4096)
    print("Reply:", reply.decode("utf-8", errors="replace"))
