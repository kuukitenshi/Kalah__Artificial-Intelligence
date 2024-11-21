from kalah import KalahState


def h_many_seeds_as_possible_in_a_pit(state: KalahState, player: int) -> int:
    pieces = state.state
    index_player = range(0, 7) if player == state.SOUTH else range(7, 14)
    num_seeds_player_list = [pieces[i] for i in index_player[:-1]]
    max_seeds_pit_index = num_seeds_player_list.index(max(num_seeds_player_list))
    for i in index_player:
        if i == max_seeds_pit_index:
            return 1  # MANY_SEEDS_IN_PIT_POINTS -- n sei valor
    return 0


def h_save_on_left_most_pit(state: KalahState, player: int) -> float:
    leftmost_pit = state.SOUTH_SCORE_PIT - 6 if player == state.SOUTH else state.NORTH_SCORE_PIT - 6
    return state.state[leftmost_pit]


def h_self_play_again_next(state: KalahState, player: int) -> float:
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


def h_opponent_play_again_next(state: KalahState, player: int) -> int:
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


def h_seeds_diff(state: KalahState, player: int) -> float:
    index_player = range(0, 6) if player == state.SOUTH else range(7, 13)
    index_opponent = range(7, 13) if player == state.SOUTH else range(0, 6)
    seeds_player = sum(state.state[i] for i in index_player)
    seeds_opponent = sum(state.state[i] for i in index_opponent)
    return (seeds_player - seeds_opponent)


# Tenta roubar o maximo que consegue e da bonus
def h_steal_as_many_as_possible_win_condition(state: KalahState, player: int) -> float:
    pieces = state.state
    index_player = range(0, 6) if player == state.SOUTH else range(7, 13)
    index_opponent = range(7, 13) if player == state.SOUTH else range(0, 6)
    score = 0

    north_kalah = state.NORTH_SCORE_PIT
    south_kalah = state.SOUTH_SCORE_PIT
    kalah_player = pieces[south_kalah] if player == state.SOUTH else pieces[north_kalah]
    kalah_opponent = pieces[north_kalah] if player == state.SOUTH else pieces[south_kalah]

    for i in index_player:
        num_seeds = pieces[i]
        end = i + num_seeds
        if num_seeds > 0 and end in index_player and pieces[end] == 0:
            mirror_opp_index = index_opponent[len(index_opponent) - 1 - index_player.index(end)]
            if pieces[mirror_opp_index] != 0:
                # Se tiver a perder e conseguir empatar/ficar a ganhar prioritizar essa jogada
                if kalah_player < kalah_opponent <= kalah_player + pieces[mirror_opp_index] + 1:
                    score += 1.2
                else:
                    score += 1
    return score


# Tenta impedir ao máximo que o oponente roube e da bonus
def h_avoid_steals_as_many_as_possible_win_condition(state: KalahState, player: int) -> float:
    pieces = state.state
    index_player = range(0, 6) if player == state.SOUTH else range(7, 13)
    index_opponent = range(7, 13) if player == state.SOUTH else range(0, 6)
    score = 0

    north_kalah = state.NORTH_SCORE_PIT
    south_kalah = state.SOUTH_SCORE_PIT
    kalah_player = pieces[south_kalah] if player == state.SOUTH else pieces[north_kalah]
    kalah_opponent = pieces[north_kalah] if player == state.SOUTH else pieces[south_kalah]

    for i in index_opponent:
        num_seeds = pieces[i]
        end = i + num_seeds
        if num_seeds > 0 and end in index_opponent and pieces[end] == 0:  # nao inclui kalah do player
            mirror_opp_index = index_player[len(index_player) - 1 - index_opponent.index(end)]
            if pieces[mirror_opp_index] != 0:
                # Se tiver a ganhar e o oponente empatar/ficar a ganhar evitar essa jogada
                if kalah_opponent < kalah_player <= kalah_opponent + pieces[mirror_opp_index] + 1:
                    score -= 1.2
                else:
                    score -= 1
    return score

# Tenta nao deixar buracos vazios do seu lado
def h_allow_many_moves(state: KalahState, player: int) -> float:
    pieces = state.state
    index_player = range(0, 6) if player == state.SOUTH else range(7, 13)
    index_opponent = range(7, 13) if player == state.SOUTH else range(0, 6)
    empty_player = sum(1 for i in index_player if pieces[i] == 0)
    empty_opponent = sum(1 for i in index_opponent if pieces[i] == 0)
    return empty_player - empty_opponent


# Preferir sempre jogada que permite jogar de novo
def h_play_again_new(state: KalahState, player: int) -> float:
    if state.to_move != player and state.pass_turn:
        return 1  # weight = 5
    if state.to_move == player and state.pass_turn:
        return -1
    return 0

# Tenta roubar o maximo que consegue
def h_steal_new(state: KalahState, player: int) -> float:
    pieces = state.state
    index_player = range(0, 6) if player == state.SOUTH else range(7, 13)
    index_opponent = range(7, 13) if player == state.SOUTH else range(0, 6)
    score = 0
    # Steal
    for i in index_player:
        num_seeds = pieces[i]
        end = i + num_seeds
        if num_seeds > 0 and end in index_player and pieces[end] == 0:
            mirror_opp_index = index_opponent[len(index_opponent) - 1 - index_player.index(end)]
            if pieces[mirror_opp_index] != 0:
                score += 1  # weight = 0.9
    # Avoid steal
    for i in index_opponent:
        num_seeds = pieces[i]
        end = i + num_seeds
        if num_seeds > 0 and end in index_opponent and pieces[end] == 0:  # nao inclui kalah do player
            mirror_opp_index = index_player[len(index_player) - 1 - index_opponent.index(end)]
            if pieces[mirror_opp_index] != 0:
                score -= 1  # weight = 0.9
    return score

        
        
        