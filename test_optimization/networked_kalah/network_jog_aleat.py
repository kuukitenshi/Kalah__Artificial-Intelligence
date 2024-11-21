import sys
from jogador import *
from network_kalah_client import *

jog_aleat = JogadorAleat('Jogador Aleatorio')

# Ler ip e porta da linha de comandos
argc = len(sys.argv)

if argc < 2:
    print(f'ERROR: Usage ./{sys.argv[0]} <address:port>')
    exit(-1)

address, port = tuple(sys.argv[1].split(':'))

# Iniciar o bot cliente para conectar ao servidor
network_kalah_client_start(address, int(port), jog_aleat)