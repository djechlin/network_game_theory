import networkx as nx
# import os
# import sys
# print(sys.path)

from centrality.rules import Rules
from centrality.strategy import StrategyBuilder
from centrality.player import Player
from centrality.entity import EntityType
from centrality.game import Game
from centrality.plot import Plotter

if __name__ == '__main__':

    """
    Create a game by instantiating all the helper objects
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

    strategy_builder = StrategyBuilder()

    player1 = Player()
    player1.rules = rules
    player1.type = EntityType.competitive_player
    player1.strategy = strategy_builder.get_greedy_strategy()

    player2 = Player()
    player2.rules = rules
    player2.type = EntityType.competitive_player
    player2.strategy = strategy_builder.get_greedy_strategy()

    player3 = Player()
    player3.rules = rules
    player3.type = EntityType.human
    player3.name = "Human"

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
    Replay graphically the game
    """

    plotter = Plotter()

    # plotter.plot_game(game1, interactive=False, leader_board=True, time_step=0.01)

    # Interactive mode
    plotter.plot_game(game1, interactive=True, time_step=0.01, leader_board=True, node_list=[0, 1, 2, 3, 4, 5, 6, 7])

    # Metrics

    #
    # from matplotlib.pyplot import figure, show
    # import numpy as npy
    # from numpy.random import rand
    #
    # if 1:  # picking on a scatter plot (matplotlib.collections.RegularPolyCollection)
    #
    #     x, y, c, s = rand(4, 100)
    #
    #
    #     def onpick3(event):
    #         ind = event.ind
    #         artist = event.artist
    #         print('onpick3 scatter:', ind, npy.take(x, ind), npy.take(y, ind))
    #         print(artist)
    #
    #     fig = figure()
    #     ax1 = fig.add_subplot(111)
    #     col = ax1.scatter(x, y, 100 * s, c, picker=True)
    #     # fig.savefig('pscoll.eps')
    #     fig.canvas.mpl_connect('pick_event', onpick3)
    #
    # show()


