import socket
import threading
import time
from datetime import datetime


HOST = "127.0.0.1"  #localhost padrao
PORT = 65435       #porta de comunicacao


def handle_client(conn):
    global f_monit
    hora = datetime.now().strftime("%H:%M:%S")




    conn.sendall(f"{hora}:conectado!! \n\t saindo...".encode())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("server esperando conexao...")
    conn, addr = s.accept()
   
    handle_client(conn)
