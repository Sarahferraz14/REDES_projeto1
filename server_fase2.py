import socket
import threading
import os
import psutil
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000


def monitor(conn, tipo, intervalo, parar):
    try:
        while not parar.is_set():
            if tipo == "CPU":
                valor = psutil.cpu_percent()
                conn.sendall(f"CPU: {valor}% usada\n".encode())

            elif tipo == "MEMORIA":
                valor = psutil.virtual_memory().percent
                conn.sendall(f"MEMORIA: {valor}% usada\n".encode())

            elif tipo == "DISCO":
                uso = psutil.disk_usage(os.path.abspath(os.sep))
                conn.sendall(f"DISCO: {uso.percent}% usado\n".encode())

            parar.wait(intervalo)  
    except OSError:
        pass  


def handle_client(conn, addr):
    print(f"cliente {addr} conectado!")
    parar = threading.Event()

    try:
        hora = datetime.now().strftime("%H:%M:%S")
        conn.sendall(
            f"{hora}:conectado!!\n"
            "comandos: CPU-n / MEMORIA-n / DISCO-n / QUIT / EXIT\n\tn=segundos para atualizar".encode()
            )

        while True:
            comando = conn.recv(1024).decode().strip().upper()
            if not comando:
                break

            if comando == "EXIT":
                break

            elif comando == "QUIT":
                parar.set()                
                parar = threading.Event()  

            elif comando.startswith("CPU-") or comando.startswith("MEMORIA-") or comando.startswith("DISCO-"):
                tipo, seg = comando.split("-", 1)

                if not seg.isdigit():
                    conn.sendall(f"erro: '{seg}' nao e um numero valido. use por exemplo CPU-3\n".encode())
                    continue

                t = threading.Thread(target=monitor, args=(conn, tipo, int(seg), parar), daemon=True)
                t.start()

    except OSError:
        pass 

    finally:
        parar.set()
        conn.close()
        print(f"cliente {addr} desconectado")


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen(5)
print("servidor esperando conexoes (sem limite de clientes ainda)...")

while True:
    conn, addr = servidor.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
