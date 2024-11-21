from kalah import KalahState


# Limpa o buraco mais a direita
def h_self_clear_rightmost_pit(state: KalahState, player: int) -> float:
    pieces = state.state
    rightmost_pit = state.SOUTH_SCORE_PIT - 1 if player == state.SOUTH else state.NORTH_SCORE_PIT - 1
    if pieces[rightmost_pit] == 0:
        return 1
    return 0


# Tenta roubar o maximo que consegue
def h_steal_as_many_as_possible(state: KalahState, player: int) -> float:
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
def h_avoid_steals_as_many_as_possible(state: KalahState, player: int) -> float:
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
def h_kalah_difference(state: KalahState, player: int) -> float:
    pits = state.state
    north_kalah = state.NORTH_SCORE_PIT
    south_kalah = state.SOUTH_SCORE_PIT
    kalah_player = pits[south_kalah] if player == state.SOUTH else pits[north_kalah]
    kalah_opponent = pits[north_kalah] if player == state.SOUTH else pits[south_kalah]
    return kalah_player - kalah_opponent


# Preferir sempre jogada que permite jogar de novo
def h_play_again(state: KalahState, player: int) -> float:
    if state.to_move != player and state.pass_turn:
        return 1
    return 0

ALL_GOOD_HEURISTICS = [h_kalah_difference, h_avoid_steals_as_many_as_possible, h_steal_as_many_as_possible,
                       h_play_again, h_self_clear_rightmost_pit]
