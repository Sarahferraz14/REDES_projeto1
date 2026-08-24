import socket
import threading




HOST = "127.0.0.1"
PORT = 65435




sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
print(sock.recv(1024).decode())