import numpy as np
import matplotlib.pyplot as plt

from game import *
from random import randint
import networkx as nx
import random

rules = Rules()
rules.nb_max_step = 2000
rules.nb_players = 1000

game = Game()
game.rules = rules
strategy_builder = StrategyBuilder()

def create_player(name, eps=.3, delta=.3):
    player = Player()
    player.rules = rules
    player.name = name
    player.type = EntityType.competitive_player
    player.strategy = strategy_builder.get_approx_greedy_strategy(EPSILON=eps, DELTA=delta)
    return player

def add_players(game, players):
    for player in players:
        game.add_player(game)
    return game

for i in range(50):
    player = create_player("Player {}".format(i), eps=.2, delta=.05)
    print("Created player {}".format(i))
    game.add_player(player)
    print("Added player {} to the game".format(i))


game.initialize_graph()
print("Graph initialized, starting game")

for i in range(rules.nb_max_step):
    print("Round {}".format(i))
    game.play_round()

game.save("history/history_1000_50active.pickle")

plotter = Plotter()
plotter.plot_game(game, interactive=False)