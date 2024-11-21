# from bot_andre import *
from segfault_good_heuristics import *
from segfault_testing_heuristics import *
from jogador import *
from torneio import *

weights_genetic_2 = [4.8422881, 3.37655866, 0.45289808, 5.47631696, 3.35868227]

best_segfault_funs = ALL_GOOD_HEURISTICS + [h_self_play_again_next, h_opponent_play_again_next, h_save_on_left_most_pit]
best_segfault_weights = weights_genetic_2 + [3.51522002, 4.18562001, 0.74147143]
# best_segfault = WeightedPlayer('best segfault', 6, best_segfault_funs, best_segfault_weights)

best_segfault_2_funs = ALL_GOOD_HEURISTICS + [h_self_play_again_next, h_opponent_play_again_next]
best_segfault_2_weights = weights_genetic_2 + [3.06036821, 6.12090023]
# best_segfault_2 = WeightedPlayer('best_segfault 2', 6, best_segfault_2_funs, best_segfault_2_weights)

# test_bot_andre_12_1 = JogadorAlfaBeta('andre 12_1', 6, func_24_12_1)

# test_bot_andre_13 = JogadorAlfaBeta('andre 13', 6, func_24_13)

for d in [3, 4, 5, 6, 7, 8]:
    print('-'*10, '[ DEPTH=', d, ' ]', '-'*10, sep='')
    old_segfault = WeightedPlayer('old segfault', d, ALL_GOOD_HEURISTICS, weights_genetic_2)
    best_segfault = WeightedPlayer('segfault 3h', d, best_segfault_funs, best_segfault_weights)
    best_segfault_2 = WeightedPlayer('segfault 2', d, best_segfault_2_funs, best_segfault_2_weights)

    test_bot_andre_12_1 = JogadorAlfaBeta('andre 12_1', d, func_24_12_1)
    test_bot_andre_13 = JogadorAlfaBeta('andre 13', d, func_24_13)
    for _ in range(3):
        print(torneio(100, [old_segfault, best_segfault, best_segfault_2, test_bot_andre_12_1, test_bot_andre_13]))