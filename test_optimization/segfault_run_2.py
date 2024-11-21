from segfault_good_heuristics import *
from segfault_testing_heuristics import *
from jogador import *
from torneio import *

if __name__ == '__main__':
    weights_g2 = [4.8422881, 3.37655866, 0.45289808, 5.47631696, 3.35868227]

    weights_3h = weights_g2 + [3.51522002, 4.18562001, 0.74147143]
    heuristics_3h = ALL_GOOD_HEURISTICS + [h_self_play_again_next, h_opponent_play_again_next, h_save_on_left_most_pit]

    weights_2h = weights_g2 + [3.06036821, 6.12090023]
    heuristics_2h = ALL_GOOD_HEURISTICS + [h_self_play_again_next, h_opponent_play_again_next]

    for d in range(3, 7):
        print('-'*10, '[ DEPTH=', d, ' ]', '-'*10, sep='')
        segfault_g2 = WeightedPlayer('G2', d, ALL_GOOD_HEURISTICS, weights_g2)
        segfault_3h = WeightedPlayer('3H', d, heuristics_3h, weights_3h)
        segfault_2h = WeightedPlayer('2H', d, heuristics_2h, weights_2h)

        for _ in range(10):
            res = torneio(100, [segfault_g2, segfault_2h, segfault_3h])
            res_sorted = sorted(res.items(), key=lambda x: x[1], reverse=True)
            print(res_sorted)
