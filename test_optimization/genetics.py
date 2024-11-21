import pygad
import sys
from torneio import *
from jogador import *
from segfault_good_heuristics import *
from segfault_testing_heuristics import *
import timeit

argc = len(sys.argv)

h_test_func = [h_self_play_again_next, h_opponent_play_again_next, h_save_on_left_most_pit, h_many_seeds_as_possible_in_a_pit]

test_funs = ALL_GOOD_HEURISTICS + h_test_func


kalah_diff_weight = 1
avoid_steal_weight = 0.9
steal_weight = 0.9
play_again_weight = 5
clear_rightmost_weight = 0.8

# weights = [kalah_diff_weight, avoid_steal_weight, steal_weight, play_again_weight, clear_rightmost_weight]
# weights = [clear_rightmost_weight, steal_weight, avoid_steal_weight, kalah_diff_weight, play_again_weight]

weights = [4.8422881, 3.37655866, 0.45289808, 5.47631696, 3.35868227] # Genetic 2 weights
best_segfault = WeightedPlayer('GENETIC 2', 6, ALL_GOOD_HEURISTICS, weights)

fitness_counter = 0

def fitness_func(ga_instance: pygad.GA, solution, solution_idx):
    global fitness_counter
    fitness_counter += 1
    print(f'Generations completed: {ga_instance.generations_completed}')
    # print(f'Calling fitness: \n\t{ga_instance}\n\t{solution}\n\t{solution_idx}')
    test_weights = best_segfault.weights + list(solution)
    test_segfault = WeightedPlayer('TEST', 6, test_funs, test_weights)
    result = torneio(100, [best_segfault, test_segfault])
    return result[test_segfault.nome] - result[best_segfault.nome]


# start = timeit.default_timer()
# torneio(100, [best_segfault, best_segfault])
# elapsed = timeit.default_timer() - start
# print(f'Elapsed: {elapsed} s')

num_generations = 7
num_parents_mating = 2
fitness_function = fitness_func
num_genes = 4
sol_per_pop = 15
init_range_low = 0.1
init_range_high = 7
parent_selection_type = 'sss'
keep_parents = -1
crossover_type = 'single_point'
mutation_type = 'random'
mutation_percent_genes = 100

ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes
                       )

print('Starting generation!')

start = timeit.default_timer()
ga_instance.run()


solution, solution_fitness, _ = ga_instance.best_solution()
print('-'*10, '[ ', test_funs, ' ]', '-'*10, sep='')
print(f'Best: {solution}')
print(f'Fitness: {solution_fitness}')
print(f'Times fitness func called: {fitness_counter}')
elapsed = timeit.default_timer() - start
print(f'Time takend {elapsed} s')