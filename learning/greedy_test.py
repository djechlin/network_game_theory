import numpy as np
import matplotlib.pyplot as plt

from game import *
from random import randint
import networkx as nx
import random
import time

rules = Rules()
rules.nb_max_step = 200
rules.nb_players = 100

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

for i in range(10):
    player = create_player("Player {}".format(i), eps=.2, delta=.05)
    print("Created player {}".format(i))
    game.add_player(player)
    print("Added player {} to the game".format(i))


game.initialize_graph()
print("Graph initialized, starting game")

for i in range(rules.nb_max_step):
    time1 = time.time()
    print("Starting round {}".format(i))
    game.play_round()
    time2 = time.time()
    print("Finished round {0} in {1} ms".format(i, (time2-time1)*1000.0))
    # save periodically
    if i % 50 == 0:
        game.save("history/history_100_10active.pickle")

game.save("history/history_100_10active.pickle")

plotter = Plotter()
plotter.plot_game(game, interactive=False)