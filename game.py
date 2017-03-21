import matplotlib.pyplot as plt
import networkx as nx
import math
from random import randint


class Rules:
    def __init__(self):
        self.nb_players = 10
        self.nb_max_step = 10


class ActivePlayer:
    def __init__(self):
        self.rules = Rules()
        self.node_id = -1
        self.name = "John"
        # self.strategy = lambda history: (randint(0, self.rules.nb_players-1), randint(0, self.rules.nb_players-1))
        self.strategy = lambda nb_nodes, node_id, history: (randint(0, self.rules.nb_players-1), randint(0, self.rules.nb_players-1))

    def get_action(self, nb_nodes, node_id, history):
        """
        Get the action exercised by the player given the current game state and his strategy
        :param history: Dict(List(edges)), history of the game (all the states of the graph up to the present moment).
        One state is a list of edges, the history uses a dictionary where the keys represent the time of the state.
        :return: edge to be modified given the strategy of the player and the current history of the game
        (wanted to only consider the current state of the game first but the teacher rightfully indicated that players
        would generally remember the previous states. Anyway, keeping track of the history is more general, allow to
        handle the visualization all at once at the end, and includes the current state, thus we could restrict
        ourselves later.)
        """
        # return self.strategy(history)
        return self.strategy(nb_nodes, node_id, history)


class Game:
    def __init__(self):
        self.rules = Rules()
        self.graph = nx.Graph()
        self.active_players = {}
        self.current_step = 0
        self.history = {}

    def initialize_graph(self):
        """
        Initialize the graph by instantiating graph nodes
        :return: void
        """
        self.graph.add_nodes_from(list(range(self.rules.nb_players)))
        self.history[0] = self.graph.edges()

    def add_player(self, player):
        """
        Add the given player to the list of active players and give it a node_id if there is still an available slot
        :param player: ActivePlayer, player to be added
        :return: void
        """
        if len(self.active_players) < self.rules.nb_players:
            node_id = len(self.active_players)
            self.active_players[node_id] = player
            player.node_id = node_id
        else:
            raise Exception("There are already too many players")

    def play_round(self):
        """
        Play one round of the game. For now, if two players are acting on the same edge, the logical OR component
        is adopted (meaning if two players want to destroy the same edge, it will get destroyed).
        No notion of edge strength and cumulative nodes strength yet
        :return: void
        """
        modified_edges = set()

        for node_id, player in self.active_players.items():
            # modified_edge = player.get_action(self.history)
            modified_edge = player.get_action(self.rules.nb_players, player.node_id, self.history)
            modified_edges.add(modified_edge)

        absent_edges = [edge for edge in modified_edges if not self.graph.has_edge(*edge)]
        existing_edges = [edge for edge in modified_edges if self.graph.has_edge(*edge)]

        self.graph.add_edges_from(absent_edges)
        self.graph.remove_edges_from(existing_edges)

        self.current_step += 1

        self.history[self.current_step] = self.graph.edges()

    def play_game(self):
        """
        Play the entire game according to the given rules (total number of steps in a game)
        :return: void
        """
        while self.current_step < self.rules.nb_max_step:
            self.play_round()


class Plotter:
    def __init__(self):
        self.alpha = 0.3
        self.round = 4
        self.color_active_player = "r"
        self.color_passive_player = "b"
        self.current_graph_when_keyboard_interactive = 0

    def plot_state(self, game):
        """
        Plot the current state of a game. Extensive use of NetworkX library, main method used is draw_networkx() and it
        is given various parameters like positions, labels, colors, sizes. The majority of the code here only computes
        those values.
        :param game: Game, current game object
        :return: void
        """
        n = game.rules.nb_players

        positions = {}
        for i in range(n):
            positions[i] = (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))

        colors = ""
        for i in range(n):
            if i in game.active_players:
                colors += self.color_active_player
            else:
                colors += self.color_passive_player

        labels = {}
        betweenness = nx.betweenness_centrality(game.graph)
        for i in range(n):
            if i in game.active_players:
                labels[i] = game.active_players[i].name + "\n" + str(round(betweenness[i], self.round))
            else:
                labels[i] = "" + "\n" + str(round(betweenness[i], self.round))

        sizes = [(10 * c + 1) * 150 for c in list(betweenness.values())]

        nx.draw_networkx(game.graph, positions, labels=labels, node_color=colors, node_size=sizes, alpha=self.alpha)
        plt.show()

    def plot_game(self, game, interactive=False):
        """
        Plot a whole game.
        :param game: Game, current game object
        :param interactive: Boolean, if false plot the history of the game, if true allow the user to navigate through
        the state
        :return: void
        """
        if interactive:

            n = game.rules.nb_players

            positions = {}
            for i in range(n):
                positions[i] = (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))

            colors = ""
            for i in range(n):
                if i in game.active_players:
                    colors += self.color_active_player
                else:
                    colors += self.color_passive_player

            graphs = []

            for round_number in range(len(game.history)):
                temp_graph = nx.Graph()
                temp_graph.add_nodes_from(game.graph.nodes())
                temp_graph.add_edges_from(game.history[round_number])

                labels = {}
                betweenness = nx.betweenness_centrality(temp_graph)
                for i in range(n):
                    if i in game.active_players:
                        labels[i] = game.active_players[i].name + "\n" + str(round(betweenness[i], self.round))
                    else:
                        labels[i] = "" + "\n" + str(round(betweenness[i], self.round))

                sizes = [(10 * c + 1) * 150 for c in list(betweenness.values())]

                graphs.append((temp_graph, labels, sizes))

            # keyboard event handler
            def key_event(e):

                if e.key == "right":
                    self.current_graph_when_keyboard_interactive += 1
                elif e.key == "left":
                    self.current_graph_when_keyboard_interactive -= 1
                else:
                    return
                self.current_graph_when_keyboard_interactive %= len(graphs)

                ax.cla()

                plt.axis([-2, 2, -2, 2])

                curr_pos = self.current_graph_when_keyboard_interactive
                nx.draw_networkx(graphs[curr_pos][0], positions, labels=graphs[curr_pos][1], node_color=colors,
                                 node_size=graphs[curr_pos][2],
                                 alpha=self.alpha)

                fig.canvas.draw()

            fig = plt.figure()

            fig.canvas.mpl_connect('key_press_event', key_event)
            ax = fig.add_subplot(111)
            plt.axis([-2, 2, -2, 2])

            nx.draw_networkx(graphs[0][0], positions, labels=graphs[0][1], node_color=colors, node_size=graphs[0][2],
                             alpha=self.alpha)

            plt.show()

        else:

            plt.ion()

            n = game.rules.nb_players

            positions = {}
            for i in range(n):
                positions[i] = (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))

            colors = ""
            for i in range(n):
                if i in game.active_players:
                    colors += self.color_active_player
                else:
                    colors += self.color_passive_player

            for round_number in range(len(game.history)):

                plt.clf()
                plt.axis([-2, 2, -2, 2])

                temp_graph = nx.Graph()
                temp_graph.add_nodes_from(game.graph.nodes())
                temp_graph.add_edges_from(game.history[round_number])

                labels = {}
                betweenness = nx.betweenness_centrality(temp_graph)
                for i in range(n):
                    if i in game.active_players:
                        labels[i] = game.active_players[i].name + "\n" + str(round(betweenness[i], self.round))
                    else:
                        labels[i] = "" + "\n" + str(round(betweenness[i], self.round))

                sizes = [(10 * c + 1) * 150 for c in list(betweenness.values())]

                nx.draw_networkx(temp_graph, positions, labels=labels, node_color=colors, node_size=sizes,
                                 alpha=self.alpha)
                plt.pause(0.05)

            while True:
                plt.pause(0.05)