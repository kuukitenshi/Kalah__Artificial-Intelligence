
# Limpa o buraco mais a direita
def h_self_clear_rightmost_pit_19(state, player):
    pieces = state.state
    rightmost_pit = state.SOUTH_SCORE_PIT - 1 if player == state.SOUTH else state.NORTH_SCORE_PIT - 1
    if pieces[rightmost_pit] == 0:
        return 1
    return 0


# Tenta roubar o maximo que consegue
def h_steal_as_many_as_possible_19(state, player):
    pieces = state.state
    index_player = range(0, 6) if player == state.SOUTH else range(7, 13)
    index_opponent = range(7, 13) if player == state.SOUTH else range(0, 6)
    score = 0
    for i in index_player:
        num_seeds = pieces[i]
        end = i + num_seeds
        if num_seeds > 0 and end in index_player and pieces[end] == 0:
            mirror_opp_index = index_opponent[len(index_opponent) - 1 - index_player.index(end)]
            if pieces[mirror_opp_index] != 0:
                score += 1
    return score


# Tenta impedir ao máximo que o oponente roube
def h_avoid_steals_as_many_as_possible_19(state, player):
    pieces = state.state
    index_player = range(0, 6) if player == state.SOUTH else range(7, 13)
    index_opponent = range(7, 13) if player == state.SOUTH else range(0, 6)
    score = 0
    for i in index_opponent:
        num_seeds = pieces[i]
        end = i + num_seeds
        if num_seeds > 0 and end in index_opponent and pieces[end] == 0:  # nao inclui kalah do player
            mirror_opp_index = index_player[len(index_player) - 1 - index_opponent.index(end)]
            if pieces[mirror_opp_index] != 0:
                score -= 1
    return score


# Maximiza a diferença entre as bolas nos kalahs
def h_kalah_difference_19(state, player):
    pits = state.state
    north_kalah = state.NORTH_SCORE_PIT
    south_kalah = state.SOUTH_SCORE_PIT
    kalah_player = pits[south_kalah] if player == state.SOUTH else pits[north_kalah]
    kalah_opponent = pits[north_kalah] if player == state.SOUTH else pits[south_kalah]
    return kalah_player - kalah_opponent


# Preferir sempre jogada que permite jogar de novo
def h_play_again_19(state, player):
    if state.to_move != player and state.pass_turn:
        return 1
    return 0


# Escolhe a jogada em que consegue jogar 2x seguidas
def h_self_play_again_next_19(state, player):
    index_player = range(0, 6) if player == state.SOUTH else range(7, 13)
    pieces = state.state
    score = 0
    score_pit = state.SOUTH_SCORE_PIT if player == state.SOUTH else state.NORTH_SCORE_PIT
    for i in index_player:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest == score_pit:
            score += 0.2
    return score


# Evita quando o oponente consegue jogar 2x seguidas
def h_opponent_play_again_next_19(state, player):
    index_opponent = range(0, 6) if player != state.SOUTH else range(7, 13)
    pieces = state.state
    score = 0
    score_pit = state.SOUTH_SCORE_PIT if player != state.SOUTH else state.NORTH_SCORE_PIT
    for i in index_opponent:
        amount = pieces[i]
        dest = i + amount
        if amount > 0 and dest == score_pit:
            score -= 0.2
    return score


# Tenta guardar as seeds no pit mais à esquerda
def h_save_on_left_most_pit_19(state, player):
    leftmost_pit = state.SOUTH_SCORE_PIT - 6 if player == state.SOUTH else state.NORTH_SCORE_PIT - 6
    return state.state[leftmost_pit]


# Função de avaliação do bot
def func_19(state, player):
    if state.is_game_over():
        result = state.result()
        return result * 10000 if player == state.SOUTH else result * -10000
    funcs = [h_kalah_difference_19, h_avoid_steals_as_many_as_possible_19, h_steal_as_many_as_possible_19,
             h_play_again_19, h_self_clear_rightmost_pit_19,
             h_self_play_again_next_19, h_opponent_play_again_next_19, h_save_on_left_most_pit_19]
    weights = [4.8422881, 3.37655866, 0.45289808, 5.47631696, 3.35868227, 3.51522002, 4.18562001, 0.74147143]
    return sum(p * f(state, player) for p, f in zip(weights, funcs))

