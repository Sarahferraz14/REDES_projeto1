# REDES_projeto1

Monitor de Sistema — Projeto Prático 1

Disciplina: Redes de Computadores Curso: Eng. Computação — PUC Campinas 

Descrição
Aplicação cliente-servidor via sockets TCP que monitora remotamente o uso de CPU, memória e disco do servidor, com comunicação bidirecional assíncrona usando threads.

Requisitos
    -> Python 3.x
    -> Biblioteca psutil:
    -> pip install psutil

Como rodar
    1. Abra dois terminais na pasta do projeto.
    2. No primeiro terminal, inicie o servidor: python S3.py
    3. No segundo terminal, inicie o cliente: python C2.py

    Comandos disponíveis (digitados no cliente)              O que faz
    --------------------------------------------------------------------------------------------------------
        CPU-n	                                             Mostra uso de CPU a cada n segundos
        MEMORIA-n	                                         Mostra uso de memória a cada n segundos
        DISCO-n	                                             Mostra uso de disco a cada n segundos
        QUIT	                                             Interrompe os monitoramentos ativos
        EXIT	                                             Encerra a conexão e sai do cliente 
    --------------------------------------------------------------------------------------------------------

Autores
Maria Eduarda Trevisan              (RA 24000309)
Sarah Mendes Ferraz                 (RA 24002927)
Renato Henrique Ykutake Florencio   (RA 24014446) 
