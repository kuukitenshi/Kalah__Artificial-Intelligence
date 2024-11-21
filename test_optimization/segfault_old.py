from jogador import *
from kalah import *



# vitoria > 1000 pontos
# derrota > -1000 pontos
# dif kalah > 2 pontos / semente
# dif pecas > 1 ponto / semente
# se formos jogador outra vez > 10 pontos, 0 caso contrario
# se o oponente conseguir jogador outra > -10 por cada buraco
# se o oponente consegue colocar num buraco vazio > -15 e -3 por cada peca

#-------------------------------------------------------------


# vitoria > 1000 pontos
# derrota > -1000 pontos
# dif kalah > 2 pontos / semente
# dif pecas > 1 ponto / semente
def func_segfault_1_19(state: KalahState, player):
    if state.is_game_over():
        aux = state.result()
        return aux*1000 if player == state.SOUTH else aux*-1000

    score = 0
    pieces = state.state

    index_player = range(0, 7) if player == state.SOUTH else range(7, 14)
    index_opponent = range(0, 7) if player != state.SOUTH else range(7, 14)

    kalah_player = pieces[index_player[-1]]
    kalah_opponent = pieces[index_opponent[-1]]
    score += (kalah_player - kalah_opponent) * 2

    pieces_player = sum(pieces[i] for i in index_player[:-1])
    pieces_opponent = sum(pieces[i] for i in index_opponent[:-1])

    score += pieces_player - pieces_opponent

    return score


segfault6_1 = JogadorAlfaBeta("Segfault_1 6",6,func_segfault_1_19)


# PIOR COM: - diferenca do seg1; - pass turn
# Tenta nao deixar roubar
def func_segfault_2_19(state: KalahState, player, verbose=False):

    if state.is_game_over():
        result1 = state.result()
        score1 = result1 * 1000 if player == state.SOUTH else result1 * -1000
        return score1

    score = 0
    pieces = state.state
    index_player = range(0, 7) if player == state.SOUTH else range(7, 14)
    index_opponent = range(7, 14) if player == state.SOUTH else range(0, 7)

    kalah_player = pieces[index_player[-1]]
    kalah_opponent = pieces[index_opponent[-1]]
    kalah_diff = (kalah_player - kalah_opponent) * 2
    score += kalah_diff

    for i in index_opponent[:-1]:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest in index_opponent:
            if dest == index_opponent[-1]:
                play_again_diff = 2 + 3
                score -= play_again_diff
            elif pieces[dest] == 0:
                dest_index = index_opponent.index(i)
                captured_pieces = pieces[index_player[len(index_player) - 2 - dest_index]]
                if captured_pieces > 0:
                    capture_diff = 2 * captured_pieces
                    score -= capture_diff
    return score


segfault6_2 = JogadorAlfaBeta("Segfault_2 6",6, func_segfault_2_19)



#-----------------------------------------------------------------------------------------------------------------------

#Não deixa roubar e tenta roubar o maximo que der
def func_segfault_3_19(state: KalahState, player, verbose=False):
    if state.is_game_over():
        result1 = state.result()
        score1 = result1 * 1000 if player == state.SOUTH else result1 * -1000
        return score1
    score = 0
    pieces = state.state

    index_player = range(0, 7) if player == state.SOUTH else range(7, 14)
    index_opponent = range(7, 14) if player == state.SOUTH else range(0, 7)

    kalah_player = pieces[index_player[-1]]
    kalah_opponent = pieces[index_opponent[-1]]
    kalah_diff = (kalah_player - kalah_opponent) * 2
    score += kalah_diff

    for i in index_opponent[:-1]:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest in index_opponent:
            if dest == index_opponent[-1]:
                play_again_diff = 2 + 3
                score -= play_again_diff
            elif pieces[dest] == 0:
                dest_index = index_opponent.index(i)
                captured_pieces = pieces[index_player[len(index_player) - 2 - dest_index]]
                if captured_pieces > 0:
                    capture_diff = 2 * captured_pieces
                    score -= capture_diff

    for i in index_player[:-1]:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest in index_player:
            if dest == index_player[-1]:
                play_again_diff = 2 + 3
                score += play_again_diff
            elif pieces[dest] == 0:
                dest_index = index_player.index(i)
                captured_pieces = pieces[index_opponent[len(index_opponent) - 2 - dest_index]]
                if captured_pieces > 0:
                    capture_diff = 2 * captured_pieces
                    score += capture_diff
    return score


segfault6_3 = JogadorAlfaBeta("Segfault_3 6",6, func_segfault_3_19)

#-----------------------------------------------------------------------------------------------------------------------


# Não deixa roubar e tenta roubar o maximo que der
# Tem pass turn - tenta jogar outra vez
# mim as vezes q o outro pode jogar again
def func_segfault_4_19(state: KalahState, player, verbose=False):
    if state.is_game_over():
        result1 = state.result()
        score1 = result1 * 1000 if player == state.SOUTH else result1 * -1000
        return score1
    score = 0
    pieces = state.state

    index_player = range(0, 7) if player == state.SOUTH else range(7, 14)
    index_opponent = range(7, 14) if player == state.SOUTH else range(0, 7)

    kalah_player = pieces[index_player[-1]]
    kalah_opponent = pieces[index_opponent[-1]]
    kalah_diff = (kalah_player - kalah_opponent) * 2
    score += kalah_diff

    if state.pass_turn and state.to_move != player:
        score += 300 #FIXME: ver bem isto nem sempre e melhor -------

    for i in index_opponent[:-1]:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest in index_opponent:
            if dest == index_opponent[-1]:
                play_again_diff = 2 + 3
                score -= play_again_diff
            elif pieces[dest] == 0:
                dest_index = index_opponent.index(i)
                captured_pieces = pieces[index_player[len(index_player) - 2 - dest_index]]
                if captured_pieces > 0:
                    capture_diff = 2 * captured_pieces
                    score -= capture_diff

    for i in index_player[:-1]:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest in index_player:
            if dest == index_player[-1]:
                play_again_diff = 2 + 3
                score += play_again_diff
            elif pieces[dest] == 0:
                dest_index = index_player.index(i)
                captured_pieces = pieces[index_opponent[len(index_opponent) - 2 - dest_index]]
                if captured_pieces > 0:
                    capture_diff = 2 * captured_pieces
                    score += capture_diff
    return score

segfault6_4 = JogadorAlfaBeta("Segfault_4 6",6, func_segfault_4_19)

#-----------------------------------------------------------------------------------------------------------------------


# igual ao 4 mas com valores mais balanceados de captura e turn
def func_segfault_5_19(state: KalahState, player):
    if state.is_game_over():
        result1 = state.result()
        score1 = result1 * 1000 if player == state.SOUTH else result1 * -1000
        return score1
    score = 0
    pieces = state.state

    index_player = range(0, 7) if player == state.SOUTH else range(7, 14)
    index_opponent = range(7, 14) if player == state.SOUTH else range(0, 7)

    kalah_player = pieces[index_player[-1]]
    kalah_opponent = pieces[index_opponent[-1]]
    kalah_diff = (kalah_player - kalah_opponent) * 2 #2
    score += kalah_diff

    if state.pass_turn and state.to_move != player:
        # next_state = state.make_move(-1)
        # score += func_segfault_5_19(next_state, player)
        score += 300

    for i in index_opponent[:-1]:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest in index_opponent:
            if dest == index_opponent[-1]:
                play_again_diff = 3
                score -= play_again_diff
            elif pieces[dest] == 0:
                dest_index = index_opponent.index(i)
                captured_pieces = pieces[index_player[len(index_player) - 2 - dest_index]]
                if captured_pieces > 0:
                    capture_diff = 2 * captured_pieces
                    score -= capture_diff

    for i in index_player[:-1]:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest in index_player:
            if dest == index_player[-1]:
                play_again_diff = 3
                score += play_again_diff
            elif pieces[dest] == 0:
                dest_index = index_player.index(i)
                captured_pieces = pieces[index_opponent[len(index_opponent) - 2 - dest_index]]
                if captured_pieces > 0:
                    capture_diff = 2 * captured_pieces
                    score += capture_diff
    return score

segfault6_5 = JogadorAlfaBeta("Segfault_5 6",6, func_segfault_5_19)


# -------------------------------------------------------------------------------------------


#melhores valores no roubo
def func_segfault_6_19(state: KalahState, player):
    if state.is_game_over():
        result1 = state.result()
        score1 = result1 * 1000 if player == state.SOUTH else result1 * -1000
        return score1
    score = 0
    pieces = state.state

    index_player = range(0, 7) if player == state.SOUTH else range(7, 14)
    index_opponent = range(7, 14) if player == state.SOUTH else range(0, 7)

    kalah_player = pieces[index_player[-1]]
    kalah_opponent = pieces[index_opponent[-1]]
    kalah_diff = (kalah_player - kalah_opponent) * 2 #2
    score += kalah_diff

    if state.pass_turn and state.to_move != player:
        score += 300

    for i in index_opponent[:-1]:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest in index_opponent:
            if dest == index_opponent[-1]:
                play_again_diff = 2
                score -= play_again_diff
            elif pieces[dest] == 0:
                dest_index = index_opponent.index(i)
                captured_pieces = pieces[index_player[len(index_player) - 2 - dest_index]]
                if captured_pieces > 0:
                    capture_diff = 0.1 * captured_pieces
                    score -= capture_diff

    for i in index_player[:-1]:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest in index_player:
            if dest == index_player[-1]:
                play_again_diff = 2
                score += play_again_diff
            elif pieces[dest] == 0:
                dest_index = index_player.index(i)
                captured_pieces = pieces[index_opponent[len(index_opponent) - 2 - dest_index]]
                if captured_pieces > 0:
                    capture_diff = 0.1 * captured_pieces
                    score += capture_diff
    return score

segfault6_6 = JogadorAlfaBeta("Segfault_6 6",6, func_segfault_6_19)

#-----------------------------------------------------------------------------------------------------------------------


#roubar com kahlas ponderados
def func_segfault_7_19(state: KalahState, player):
    if state.is_game_over():
        result1 = state.result()
        score1 = result1 * 1000 if player == state.SOUTH else result1 * -1000
        return score1
    score = 0
    pieces = state.state

    index_player = range(0, 7) if player == state.SOUTH else range(7, 14)
    index_opponent = range(7, 14) if player == state.SOUTH else range(0, 7)

    kalah_player = pieces[index_player[-1]]
    kalah_opponent = pieces[index_opponent[-1]]
    kalah_diff = (kalah_player - kalah_opponent) * 2 #2
    score += kalah_diff

    if state.pass_turn and state.to_move != player:
        score += 300

    for i in index_opponent[:-1]:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest in index_opponent:
            if dest == index_opponent[-1]:
                play_again_diff = 2
                score -= play_again_diff
            elif pieces[dest] == 0:
                dest_index = index_opponent.index(i)
                captured_pieces = pieces[index_player[len(index_player) - 2 - dest_index]] + 1
                if captured_pieces > 1:
                    captured_kalah = kalah_opponent + captured_pieces
                    if kalah_diff > 0 and captured_kalah > kalah_player: # tava a ganhar e deixa de tar
                        score -= 5 + (captured_kalah - kalah_player) * 0.2
                    elif kalah_diff > 0 and captured_kalah < kalah_player: # tava a ganhar e continua
                        score -= 1 + captured_pieces * 0.1
                    else:
                        score -= 2 + captured_pieces * 0.15

    for i in index_player[:-1]:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest in index_player:
            if dest == index_player[-1]:
                play_again_diff = 2
                score += play_again_diff
            elif pieces[dest] == 0:
                dest_index = index_player.index(i)
                captured_pieces = pieces[index_opponent[len(index_opponent) - 2 - dest_index]] + 1
                if captured_pieces > 1:
                    captured_kalah = kalah_opponent + captured_pieces
                    if kalah_diff > 0 and captured_kalah > kalah_player:  # tava a ganhar e deixa de tar
                        score += 5 + (captured_kalah - kalah_player) * 0.2
                    elif kalah_diff > 0 and captured_kalah < kalah_player:  # tava a ganhar e continua
                        score += 1 + captured_pieces * 0.1
                    else:
                        score += 2 + captured_pieces * 0.15
    return score

segfault6_7 = JogadorAlfaBeta("Segfault_7 6",6, func_segfault_7_19)