from jogador import *

#tenta maximizar a diferença entre o número das suas sementes (no 6 poços e armazém)
# e as do seu adversário quando o jogo não é final. Quando o jogo é final, +100 para
# a vitória, -100 para a derrota e 0 para o empate.
def chapiteu_func(state, player):
    if state.is_game_over():
        result = state.result()
        return result*100 if player == state.SOUTH else result*-100
    pieces = state.state
    # 0-6 SOUTH
    # 7-13 NORTH
    player_count = sum(pieces[i] for i in range(14) if player == state.SOUTH and i < 7 or player == state.NORTH and i >= 7)
    opponent_count = sum(pieces[i] for i in range(14) if player == state.SOUTH and i >= 7 or player == state.NORTH and i < 7)
    return player_count - opponent_count

chapiteu_6 = JogadorAlfaBeta('Chapiteu 6', 6, chapiteu_func)