import networkx as nx
# import os
# import sys
# print(sys.path)

import datetime

from centrality.rules import Rules
from centrality.strategy import Strategy
from centrality.player import Player
from centrality.entity import EntityType
from centrality.game import Game
from centrality.plot import Plotter

if __name__ == '__main__':

    """
    Create rules and game
    """

    rules = Rules()
    rules.nb_max_step = 10

    game1 = Game()
    game1.rules = rules

    """
    Create some players and add them to the game
    After having initialized the graph so that
    every player receives an id, add some impossible edges
    """

    player1 = Player(rules=rules, type=EntityType.competitive_player, name="John", strategy_type=Strategy.greedy)
    player2 = Player(rules=rules, type=EntityType.competitive_player, name="Jake", strategy_type=Strategy.greedy)
    player3 = Player(rules=rules, type=EntityType.human, name="Pierre")

    game1.add_player(player1)
    game1.add_player(player2)
    # game1.add_player(player3)

    game1.initialize_graph()

    game1.impossible_edges = [(player1.node_id, player2.node_id), (player2.node_id, player1.node_id)]

    """
    Play the game
    """

    game1.play_game()

    """
    Save the game
    """

    date = datetime.datetime.now()
    game1.save(filename="games/" + str(date) + ".pkl")

    """
    Load the game
    """

    game = Game()
    game.load('history.pickle')

    """
    Replay the game
    """

    plotter = Plotter()
    plotter.plot_game(game, interactive=False, leader_board=True, time_step=0.01)

    # Interactive mode
    # plotter.plot_game(game1, interactive=True, time_step=0.01, leader_board=True, node_list=[0, 1, 2, 3, 4, 5, 6, 7])

    # Metrics