import sys
from jogador import *
from network_kalah_client import *
from segfault_good_heuristics import *
from segfault_testing_heuristics import *

weights_genetic_2 = [4.8422881, 3.37655866, 0.45289808, 5.47631696, 3.35868227]

best_segfault_funs = ALL_GOOD_HEURISTICS + [h_self_play_again_next, h_opponent_play_again_next]
best_segfault_weights = weights_genetic_2 + [3.06036821, 6.12090023]

best_segfault = WeightedPlayer('segfault 2h', 6, best_segfault_funs, best_segfault_weights)


# Ler ip e porta da linha de comandos
argc = len(sys.argv)

if argc < 2:
    print(f'ERROR: Usage ./{sys.argv[0]} <address:port>')
    exit(-1)

address, port = tuple(sys.argv[1].split(':'))

# Iniciar o bot cliente para conectar ao servidor
network_kalah_client_start(address, int(port), best_segfault)