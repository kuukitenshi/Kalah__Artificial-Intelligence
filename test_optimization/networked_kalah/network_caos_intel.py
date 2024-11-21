import sys
from jogador import *
from network_kalah_client import *

# Função de avaliação do el caos intel
def f_caos_intel(estado,jogador):
    """Quando é terminal: +100 para vitória, -100 para a derrota e 0 para o empate.
       Quando o tabuleiro é não terminal devolve 0, o que quer dizer que como o minimax baralha as acções, será random"""
    if estado.is_game_over():
        aux = estado.result()
        return aux*100 if jogador == estado.SOUTH else aux*-100
    return 0

# Criar jogador alfa beta
el_caos_int6=JogadorAlfaBeta("El Caos Inteligente 6",6,f_caos_intel)

# Ler ip e porta da linha de comandos
argc = len(sys.argv)

if argc < 2:
    print(f'ERROR: Usage ./{sys.argv[0]} <address:port>')
    exit(-1)

address, port = tuple(sys.argv[1].split(':'))

# Iniciar o bot cliente para conectar ao servidor
network_kalah_client_start(address, int(port), el_caos_int6)