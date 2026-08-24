import socket
import threading
import time
import psutil
import os  
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
            conn.sendall(f"CPU: {valor}% usada\n".encode())
        elif tipo == "MEMORIA":                                 #passa infos da MEMORIA qndo cliente pede
            valor = psutil.virtual_memory().percent            
            conn.sendall(f"MEMORIA: {valor}% usada\n".encode())
        elif tipo == "DISCO":
            uso = psutil.disk_usage(os.path.abspath(os.sep))
            conn.sendall(f"DISCO: {uso.percent}% usado\n".encode())
       
        time.sleep(intervalo)




def handle_client(conn):
    global f_monit
    hora = datetime.now().strftime("%H:%M:%S")
    conn.sendall(f"{hora}:conectado!!\ncomandos: CPU-n / MEMORIA-n / DISCO-n / QUIT / EXIT\n\tn=segundos para atualizar".encode())




    while True:
        comando = conn.recv(1024).decode().strip().upper()
        if not comando:
            break




        if comando == "EXIT":
            f_monit = True
            conn.sendall(f"saindo...".encode())
            break




        elif comando == "QUIT":
            f_monit = True




        elif comando.startswith("CPU-") or comando.startswith("MEMORIA-") or comando.startswith("DISCO-"):
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
