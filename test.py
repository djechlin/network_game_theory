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


def greedy(nb_nodes, node_id, history):
    graph = nx.Graph()
    graph.add_nodes_from(list(range(nb_nodes)))
    graph.add_edges_from(history[len(history)-1])

    # wont decrease betweenness, better if allowed to play blank move (not doing anything)
    # best_u, best_v, best_bet = 0, 0, nx.betweenness_centrality(graph)[node_id]

    # start best betweenness at 0 to find the best move (even if it means decreasing the current betweenness)
    best_u, best_v, best_bet = 0, 0, 0

    for i in range(nb_nodes):
        for j in range(nb_nodes):
            # Don't want links from node to same node to interfere
            if j == i:
                pass
            else:
                if graph.has_edge(i, j):
                    graph.remove_edge(i, j)

                    new_bet = nx.betweenness_centrality(graph)[node_id]
                    if new_bet > best_bet:
                        best_u, best_v, best_bet = i, j, new_bet

                    graph.add_edge(i, j)

                else:
                    graph.add_edge(i, j)

                    new_bet = nx.betweenness_centrality(graph)[node_id]
                    if new_bet > best_bet:
                        best_u, best_v, best_bet = i, j, new_bet

                    graph.remove_edge(i, j)

    while best_u == best_v:
        best_u, best_v = node_id, randint(0, nb_nodes)

    return best_u, best_v

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

player3 = ActivePlayer()
player3.rules = rules
player3.strategy = greedy

player4 = ActivePlayer()
player4.rules = rules
player4.strategy = greedy

game1.add_player(player3)
game1.add_player(player4)

game1.initialize_graph()

game1.play_game()

print(game1.history[8])

plotter = Plotter()
plotter.plot_game(game1, interactive=True)


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
