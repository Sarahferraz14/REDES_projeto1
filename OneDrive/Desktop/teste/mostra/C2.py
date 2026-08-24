import socket
import threading


HOST = "127.0.0.1"
PORT = 65435




def recebe(sock):
    while True:
        dado = sock.recv(1024).decode()
        if not dado:
            break
        print(dado, end="")




def envia(sock):
    while True:
        comando = input()
        sock.sendall(comando.encode())
        if comando.strip().upper() == "EXIT":
            break




sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
print(sock.recv(1024).decode())


t1 = threading.Thread(target=envia, args=(sock,), daemon=True)
t2 = threading.Thread(target=recebe, args=(sock,), daemon=True)
t1.start()
t2.start()
t1.join()


