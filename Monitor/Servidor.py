import socket
import threading
import os
import sys
import psutil
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

clientes = []
lock = threading.Lock()


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
        # cliente caiu / fechou a conexao no meio do envio: so encerra a thread,
        # sem derrubar o servidor nem imprimir traceback
        pass


def handle_client(conn, addr, limite):
    eu = threading.current_thread()

    with lock:
        if len(clientes) >= limite:
            lotado = True
        else:
            clientes.append(eu)
            lotado = False

    if lotado:
        try:
            conn.sendall("limite de clientes atingido!\n\ttente novamente mais tarde.\n".encode())
        except OSError:
            pass  # cliente ja tinha desistido/caido antes de receber o aviso
        finally:
            conn.close()
        return

    print(f"cliente {addr} conectado ({len(clientes)}/{limite})")
    parar = threading.Event()

    try:
        hora = datetime.now().strftime("%H:%M:%S")
        conn.sendall(
            f"{hora}:conectado!!\n"
            "comandos: CPU-n / MEMORIA-n / DISCO-n / QUIT / EXIT\n\tn=segundos para atualizar".encode()
        )
        while True:
            dados = conn.recv(1024)
            if not dados:
                # cliente derrubou a conexao sem mandar EXIT (fechou a janela, caiu a rede, etc.)
                break

            try:
                comando = dados.decode().strip().upper()
            except UnicodeDecodeError:
                # recebeu bytes que nao formam texto valido: ignora e segue esperando
                continue
            if not comando:
                continue

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
        # erro de conexao com esse cliente especifico (reset, pipe quebrado, etc.):
        # so esse atendimento termina, o servidor continua rodando para os outros
        pass

    finally:
        parar.set()
        conn.close()
        with lock:
            if eu in clientes:
                clientes.remove(eu)
        print(f"Cliente {addr} desconectado ({len(clientes)}/{limite})")


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Uso: python server_fase3.py <limite_de_clientes>")
        sys.exit(1)
    limite = int(sys.argv[1])

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((HOST, PORT))
        servidor.listen(5)
    except OSError as e:
        print(f"Nao foi possivel iniciar o servidor na porta {PORT}: {e}")
        sys.exit(1)

    print(f"Servidor esperando conexoes (limite: {limite} clientes)...")

    try:
        while True:
            try:
                conn, addr = servidor.accept()
            except OSError:
                # problema pontual ao aceitar uma conexao: nao derruba o servidor
                continue
            threading.Thread(target=handle_client, args=(conn, addr, limite), daemon=True).start()
    except KeyboardInterrupt:
        print("\nEncerrando servidor (Ctrl+C)...")
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
