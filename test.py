from game import *
from random import randint
import networkx as nx

"""
First test
Two active players, random strategy
"""

# rules1 = Rules()
#
# game1 = Game()
#
# player1 = ActivePlayer()
# player2 = ActivePlayer()
#
# game1.add_player(player1)
# game1.add_player(player2)
#
# game1.initialize_graph()
#
# game1.play_game()
#
# plotter = Plotter()
# plotter.plot_game(game1, interactive=True)


"""
Second test
One active player (greedy current state strategy)
"""

# rules = Rules()
# rules.nb_max_step = 20
#
# game1 = Game()
# game1.rules = rules
#
# player3 = ActivePlayer()
# player3.rules = rules
# player3.strategy = greedy
#
# game1.add_player(player3)
#
# game1.initialize_graph()
#
# game1.play_game()
#
# # print(game1.history[11])
#
# plotter = Plotter()
# plotter.plot_game(game1, interactive=True)


# Some tests

# graph_test = nx.Graph()
# graph_test.add_nodes_from(list(range(rules.nb_players)))
# graph_test.add_edges_from(game1.history[11])
# # to test if it's better to add an edge between two other nodes or remove one of ours
# graph_test.add_edge(4, 5)
#
# game_test = Game()
# game_test.graph = graph_test
# game_test.rules = rules
# game_test.active_players = {0: player3}
# game_test.current_step = 11
#
# plotter = Plotter()
# plotter.plot_state(game_test)


"""
Third test
2 actives players, greedy strategy
"""

rules = Rules()
rules.nb_max_step = 20

game1 = Game()
game1.rules = rules

player3 = Player()
player3.rules = rules
player3.type = EntityType.competitive_player
s3 = BuildingStrategy()
print(s3.get_greedy)
player3.strategy = s3.get_greedy()


player4 = Player()
player4.rules = rules
player4.type = EntityType.competitive_player
player4.strategy = s3.get_random()

game1.add_player(player3)
game1.add_player(player4)

game1.initialize_graph()

game1.play_game()

# print(game1.history[8])
# for key, player in game1.players.items():
#     print(player.type)

plotter = Plotter()
plotter.plot_game(game1, interactive=True)
# plotter.plot_state(game1)


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
