import os
import socket
import sys
import threading

HOST = "127.0.0.1"
PORT = 5000


def recebe(sock):
    while True:
        try:
            dado = sock.recv(1024).decode()
        except (OSError, UnicodeDecodeError):
            dado = ""

        if not dado:
            # servidor fechou a conexao (EXIT aceito, limite atingido, erro, etc.)
            print("Conexao encerrada.", flush=True)
            os._exit(0)
        print(dado, end="", flush=True)


def envia(sock):
    while True:
        try:
            comando = input()
        except (EOFError, KeyboardInterrupt):
            # teclado fechado ou Ctrl+C: trata como se o usuario tivesse pedido EXIT
            comando = "EXIT"

        try:
            sock.sendall(comando.encode())
        except OSError:
            # a conexao ja caiu por outro motivo (o servidor fechou, rede caiu, etc.)
            break

        if comando.strip().upper() == "EXIT":
            break


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
    except OSError as e:
        print(f"Nao foi possivel conectar ao servidor em {HOST}:{PORT} ({e}).")
        sys.exit(1)

    try:
        boas_vindas = sock.recv(1024).decode()
    except (OSError, UnicodeDecodeError):
        boas_vindas = ""

    if not boas_vindas:
        print("O servidor fechou a conexao antes de responder.")
        sock.close()
        sys.exit(1)
    print(boas_vindas)

    t1 = threading.Thread(target=envia, args=(sock,), daemon=True)
    t2 = threading.Thread(target=recebe, args=(sock,), daemon=True)
    t1.start()
    t2.start()

    try:
        while t1.is_alive():
            t1.join(0.5)
    except KeyboardInterrupt:
        print("\nEncerrando cliente...", flush=True)
        try:
            sock.sendall("EXIT".encode())
        except OSError:
            pass
        os._exit(0)

    sock.close()


if __name__ == "__main__":
    main()
