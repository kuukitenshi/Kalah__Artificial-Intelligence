import itertools
from torneio import *
from chapiteu import *
from segfault_good_heuristics import *
from segfault_testing_heuristics import *
from segfault_old import *


def test_with_different_weights(test_against_player: Jogador, funs: list, weights_list: list, depths: list, rounds: int = 100):
    game_id = random.randint(1, 254)
    print(f'GAME BOARD: {game_id}')
    for depth in depths:
        print('-'*10, '[ ', f'DEPTH = {depth}', ' ]', '-'*10, sep='')
        for weights in list(itertools.product(*weights_list)):
            test_weights = list(weights)
            test_player = WeightedPlayer(f'TEST_PLAYER w={test_weights}', depth, funs, test_weights)
            print(f'RUNNING VS {test_player.nome}')
            print(torneio(rounds, [test_against_player, test_player], game_id))
            print('')
        print('\n')


if __name__ == '__main__':
    best_segfault_funs = [h_kalah_difference, h_avoid_steals_as_many_as_possible,
                          h_steal_as_many_as_possible, h_play_again, h_self_clear_rightmost_pit]
    
    # GOOD FOR RANDOM
    kalah_diff_weight = 1
    avoid_steal_weight = 0.9
    steal_weight = 0.9
    play_again_weight = 5
    clear_rightmost_weight = 0.8

    # fist_w = [kalah_diff_weight, avoid_steal_weight, steal_weight, play_again_weight, clear_rightmost_weight]
    # best_segfault = WeightedPlayer('BEST SEGFAULT', 6, best_segfault_funs, fist_w)

    # weights1 = [3.72422002, 2.772725, 0.54114079, 9.53979447, 0.5405322]
    # gen1 = WeightedPlayer('genetic1', 6, best_segfault_funs, weights1)

    weights2 =  [4.8422881, 3.37655866, 0.45289808, 5.47631696, 3.35868227]
    gen2 = WeightedPlayer('genetic2', 6, best_segfault_funs, weights2)
    
    # weights3 = [0.20376776, 2.60935206, 6.30715144, 7.39019894, 6.08263509] #FIXME: LIXO
    # gen3 = WeightedPlayer('genetic3', 6, best_segfault_funs, weights3)

    # w_allow_many = weights2 + [0.88085673] #FIXME: LIXO
    # seg_allow_many = WeightedPlayer('genetic3_com_move_many', 6, best_segfault_funs+[h_allow_many_moves], w_allow_many)
    
    w_many_seeds_pit = weights2 + [1.27305884]
    seg_many_seeds_pit = WeightedPlayer('genetic3_many_seeds_pit', 6, best_segfault_funs+[h_many_seeds_as_possible_in_a_pit], w_many_seeds_pit)
    
    # w_seeds_diff = weights2 + [0.47197118] #FIXME: LIXO
    # seg_seeds_dif = WeightedPlayer('genetic_seeds_dif', 6, best_segfault_funs+[h_seeds_diff], w_seeds_diff)
    
    # w_save_left_most = weights2 + [1.98760131]
    # seg_save_left_most = WeightedPlayer('genetic_save_left_most', 6, best_segfault_funs+[h_save_on_left_most_pit], w_save_left_most)
    
    # w_opp_play_again_next = weights2 + [1.27651567]
    # seg_opp_play_again_next = WeightedPlayer('genetic_opp_play_again_next', 6, best_segfault_funs+[h_opponent_play_again_next], w_opp_play_again_next)
    
    # w_self_play_again_next = weights2 + [5.42259463]
    # seg_self_play_again_next = WeightedPlayer('genetic_self_play_again_next', 6, best_segfault_funs+[h_self_play_again_next], w_self_play_again_next)
    
    w_self_opp_play_again_next = weights2 + [3.06036821, 6.12090023] #ganhou 4/10 -- FIXME: tb e bom
    seg_self_opp_play_again_next = WeightedPlayer('genetic_self_opp_play_again_next', 6, best_segfault_funs+[h_self_play_again_next, h_opponent_play_again_next], w_self_opp_play_again_next)
    
    w_self_opp_play_left_most = weights2 + [3.51522002, 4.18562001, 0.74147143] #ganhou 6/10 e 5/10 --- FIXME: MELHOR ATE AGR vs gen2
    seg_self_opp_play_left_most = WeightedPlayer('genetic_self_opp_play_left_most', 6, best_segfault_funs+[h_self_play_again_next, h_opponent_play_again_next, h_save_on_left_most_pit], w_self_opp_play_left_most)
    
    # w_self_opp_play_left_most_seeds_pit = weights2 + [6.69824292, 0.42066474, 2.19157354, 0.70387147] #ganhou 4/10 e 1 empate
    # seg_self_opp_play_left_most_seeds_pit = WeightedPlayer('genetic_self_opp_play_left_most_seeds_pit', 6, best_segfault_funs+[h_self_play_again_next, h_opponent_play_again_next, h_save_on_left_most_pit, h_many_seeds_as_possible_in_a_pit], w_self_opp_play_left_most_seeds_pit)
    
    
    for x in range(10):
        print("--------------------------")
        print(torneio(100, [seg_self_opp_play_left_most, gen2, seg_self_opp_play_again_next]))
    
    # print(torneio(100, [best_segfault, segfault6_1, segfault6_2, segfault6_3,
    #                     segfault6_4, segfault6_5, segfault6_6, segfault6_7, chapiteu_6]))
    #
    # for _ in range(10):
    #     print(torneio(100, [best_segfault, best_segfault_2, chapiteu_6, best_segfault_3, segfault6_7]))

    # segfault_test_funs = [h_kalah_difference, h_avoid_steals_as_many_as_possible_win_condition,
    #                       h_steal_as_many_as_possible_win_condition, h_play_again, h_self_clear_rightmost_pit]

    # segfault_test = WeightedPlayer('SEGFAULT TEST', 6, segfault_test_funs, weights)

    # print(torneio(100, [segfault_test, best_segfault, segfault6_1, segfault6_2, segfault6_3,
    #                     segfault6_4, segfault6_5, segfault6_6, segfault6_7, chapiteu_6]))


    # #--------
    # depths = [3, 4, 5, 6, 7, 8]
    # num_torneios = 100
    # total_results = dict()
    # for d in depths:  
    #     print('-'*10, '[ ', d, ' ]', '-'*10, sep='')
    #     seg = WeightedPlayer('SEGFAULT', d, best_segfault_funs, weights)
    #     genetic1 = WeightedPlayer('Genetic 1', d, best_segfault_funs, weights2)
    #     genetic2 = WeightedPlayer('Genetic 2', d, best_segfault_funs, weights3)

    #     result = torneio(num_torneios, [seg, genetic1, genetic2])
    #     print(result)
    #     for k, v in result.items():
    #         if k not in total_results:
    #             total_results[k] = 0
    #         total_results[k] += v
    # print('-'*20)
    # print(total_results)











