from game import *
from random import randint
import networkx as nx

"""
Test
p1:
"""

rules = Rules()
rules.nb_max_step = 2

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
game1.add_player(player3)

game1.initialize_graph()

game1.play_game()

# print(BuildingStrategy.get_random_edge(10, 2))

# for key, player in game1.players.items():
#     print(player.type)
#
# for key, state in game1.history.items():
#     print(state)
#
# print(len(game1.history[len(game1.history) - 1]) )

plotter = Plotter()
plotter.plot_game(game1, interactive=True, time_step=0.01)

# plotter.plot_game(game1, interactive=True, time_step=0.01, educational=True, node_list=[0, 1, 2, 3, 4, 5, 6, 7])

# plotter.plot_state(game1, node_list=[0, 1, 2, 3, 4, 5, 6, 7])


# Some tests

# graph_test = nx.Graph()
# graph_test.add_nodes_from(list(range(rules.nb_players)))
# graph_test.add_edges_from(game1.history[8])
# # to test if it's better to add another edge that what the players are doing
# # graph_test.add_edge(4, 5)
#
# game_test = Game()
# game_test.graph = graph_test
# game_test.rules = rules
# game_test.active_players = {0: player3, 1: player4}
# game_test.current_step = 8
#
# plotter = Plotter()
# plotter.plot_state(game_test)
