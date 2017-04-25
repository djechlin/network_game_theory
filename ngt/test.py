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

    rules = Rules()
    rules.nb_max_step = 10

    game1 = Game()
    game1.rules = rules

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

    print(game1.impossible_edges)
    print(player1.node_id)
    print(player2.node_id)

    game1.play_game()

    plotter = Plotter()
    plotter.plot_game(game1, interactive=True, time_step=0.01)

    # plotter.plot_game(game1, interactive=True, time_step=0.01, leader_board=True, node_list=[0, 1, 2, 3, 4, 5, 6, 7])
