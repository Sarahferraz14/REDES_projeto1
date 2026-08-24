import socket
import threading
import time
import psutil
from datetime import datetime


HOST = "127.0.0.1"  #localhost padrao
PORT = 65435        #porta de comunicacao


f_monit = False     #flag de controle do monitoramento


def monitor(conn, tipo, intervalo):


    global f_monit
    f_monit = False


    while not f_monit:                                          #loop funciona enquanto flag for falsa
        if tipo == "CPU":                                       #passa infos da CPU qndo cliente pede
            valor = psutil.cpu_percent()
            conn.sendall(f"CPU: {valor}%\n".encode())


        time.sleep(intervalo)


def handle_client(conn):
    global f_monit
    hora = datetime.now().strftime("%H:%M:%S")
    conn.sendall(f"{hora}:conectado!!\n comandos: CPU-n /EXIT".encode())


    while True:
        comando = conn.recv(1024).decode().strip().upper()
        if not comando:
            break


        if comando == "EXIT":
            f_monit = True
            break


        elif comando.startswith("CPU-"):
            tipo, seg = comando.split("-")
            t = threading.Thread(target=monitor, args=(conn, tipo, int(seg)), daemon=True)
            t.start()


    conn.close()    


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("server esperando conexao...")
    conn, addr = s.accept()
    handle_client(conn)
