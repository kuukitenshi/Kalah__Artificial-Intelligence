from jogos import *


class Jogador():
    def __init__(self, nome, fun):
        self.nome = nome
        self.fun = fun

    def display(self):
        print(self.nome+" ")


class JogadorAleat(Jogador):

    def __init__(self, nome):
        self.nome = nome
        self.fun = lambda game, state: random.choice(game.actions(state))


class JogadorAlfaBeta(Jogador):

    def __init__(self, nome, depth,fun_eval):
        self.nome = nome
        self.fun = lambda game, state: alphabeta_cutoff_search_new(state,game,depth,eval_fn=fun_eval)


class WeightedPlayer(JogadorAlfaBeta):

    def __init__(self, nome, depth, funs: list, weights: list = None):
        super().__init__(nome, depth, self.fun_eval)
        self.funs = funs
        self.weights = weights
        if self.weights is None:
            self.weights = [1] * len(funs)

    def fun_eval(self, state, player):
        if state.is_game_over():
            result = state.result()
            return result * 10000 if player == state.SOUTH else result * -10000
        return sum(p * f(state, player) for p, f in zip(self.weights, self.funs))


class HumanPlayer(Jogador):

    def __init__(self, nome):
        self.nome = nome

    def fun(self, game, state):
        available_actions = state.get_legal_moves()
        if available_actions == [-1]:
            return -1
        print(f'Actions: {available_actions}')
        action = int(input('> '))
        while action not in available_actions:
            print('Invalid action!')
            action = int(input('> '))
        return action

