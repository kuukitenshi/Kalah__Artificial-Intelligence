import sys
from jogador import *
from network_kalah_client import *
from segfault_good_heuristics import *
from segfault_testing_heuristics import *

weights_ng = [1, 0.9, 0.9, 5, 0.8]

best_segfault = WeightedPlayer('segfault ng', 6, ALL_GOOD_HEURISTICS, weights_ng)


# Ler ip e porta da linha de comandos
argc = len(sys.argv)

if argc < 2:
    print(f'ERROR: Usage ./{sys.argv[0]} <address:port>')
    exit(-1)

address, port = tuple(sys.argv[1].split(':'))

# Iniciar o bot cliente para conectar ao servidor
network_kalah_client_start(address, int(port), best_segfault)