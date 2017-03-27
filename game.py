import matplotlib.pyplot as plt
import networkx as nx
import math
from random import randint
from enum import Enum


class Rules:
    def __init__(self):
        self.nb_players = 10
        self.nb_max_step = 10


class EntityType(Enum):
    competitive_player = 1
    non_competitive_player = 2
    other_entity = 3


class Player:
    def __init__(self, active=False):
        self.rules = Rules()
        self._type = EntityType.non_competitive_player
        self.node_id = -1
        self.name = "John"
        # self.strategy = lambda nb_nodes, node_id, history: \
        #     (randint(0, self.rules.nb_players - 1), randint(0, self.rules.nb_players - 1))
        self.strategy = lambda nb_nodes, node_id, history: None

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

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
        self.players = {}
        self.current_step = 0
        self.history = {}

    def initialize_graph(self):
        """
        Initialize the graph by instantiating graph nodes.
        By default, all the remaining nodes are non_competitive players
        :return: void
        """
        self.graph.add_nodes_from(list(range(self.rules.nb_players)))
        self.history[0] = self.graph.edges()

        while len(self.players) < self.rules.nb_players:
            temp_non_competitive_player = Player()
            self.add_player(temp_non_competitive_player)

    def add_player(self, player):
        """
        Add the given player to the list of players and give it a node_id if there is still an available slot
        :param player: Player, player to be added
        :return: void
        """
        if len(self.players) < self.rules.nb_players:
            node_id = len(self.players)
            self.players[node_id] = player
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

        for node_id, player in self.players.items():
            modified_edge = player.get_action(self.rules.nb_players, player.node_id, self.history)
            if modified_edge is not None:
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
        self.node_transparency = 0.3
        self.significant_digits = 4
        self.color_competitive_player = "r"
        self.color_non_competitive_player = "b"
        self.color_other_entity = "g"
        self.current_interactive_graph = 0  # Allow to navigate through the graphs in interactive mode

    @staticmethod
    def get_positions(self, nb_players):
        """
        Compute the positions of the players so that they are fixed when visualizing the evolution of the game
        :param nb_players: int, number of players in the game
        :return: dictionary of (x,y) coordinate tuple
        """
        positions = {}
        for i in range(nb_players):
            positions[i] = (math.cos(2 * math.pi * i / nb_players), math.sin(2 * math.pi * i / nb_players))
        return positions

    def get_colors(self, game, nb_players):
        """
        Compute the colors of the players according to their entity type to be able to easily differentiate them
        :param game: Game, played game
        :param nb_players: int, number of players in the game
        :return: string of color initials
        """
        colors = ""
        for i in range(nb_players):
            player = game.players[i]
            if player.type is EntityType.competitive_player:
                colors += self.color_competitive_player
            elif player.type is EntityType.non_competitive_player:
                colors += self.color_non_competitive_player
            else:
                colors += self.color_other_entity
        return colors

    def get_labels_size(self, game, round_number, nb_players):
        """
        Compute the labels and sizes of the players according to a given graph state (game + round number)
        :param game: Game, played game
        :param nb_players: int, number of players in the game
        :param round_number: int, time step/round number of the game
        :return: tuple containing a dictionary for the labels and an array for the sizes
        """
        temp_graph = nx.Graph()
        temp_graph.add_nodes_from(game.graph.nodes())
        temp_graph.add_edges_from(game.history[round_number])

        labels = {}
        betweenness = nx.betweenness_centrality(game.graph)
        for i in range(nb_players):
            player = game.players[i]
            if player.type is EntityType.competitive_player:
                labels[i] = game.players[i].name + "\n" + str(round(betweenness[i], self.significant_digits))
            elif player.type is EntityType.non_competitive_player:
                labels[i] = "" + "\n" + str(round(betweenness[i], self.significant_digits))
            else:
                labels[i] = "other_entity"

        sizes = [(10 * c + 1) * 150 for c in list(betweenness.values())]

        return labels, sizes

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
            player = game.players[i]
            if player.type is EntityType.competitive_player:
                colors += self.color_competitive_player
            elif player.type is EntityType.non_competitive_player:
                colors += self.color_non_competitive_player
            else:
                colors += self.color_other_entity

        labels = {}
        betweenness = nx.betweenness_centrality(game.graph)
        for i in range(n):
            player = game.players[i]
            if player.type is EntityType.competitive_player:
                labels[i] = game.players[i].name + "\n" + str(round(betweenness[i], self.significant_digits))
            elif player.type is EntityType.non_competitive_player:
                labels[i] = "" + "\n" + str(round(betweenness[i], self.significant_digits))
            else:
                labels[i] = "other_entity"

        sizes = [(10 * c + 1) * 150 for c in list(betweenness.values())]

        nx.draw_networkx(game.graph, positions, labels=labels,
                         node_color=colors, node_size=sizes, alpha=self.node_transparency)
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
                player = game.players[i]
                if player.type == EntityType.competitive_player:
                    colors += self.color_competitive_player
                elif player.type == EntityType.non_competitive_player:
                    colors += self.color_non_competitive_player
                else:
                    colors += self.color_other_entity

            graphs = []

            for round_number in range(len(game.history)):
                temp_graph = nx.Graph()
                temp_graph.add_nodes_from(game.graph.nodes())
                temp_graph.add_edges_from(game.history[round_number])

                labels = {}
                betweenness = nx.betweenness_centrality(temp_graph)
                for i in range(n):
                    player = game.players[i]
                    if player.type is EntityType.competitive_player:
                        labels[i] = game.players[i].name + "\n" + str(round(betweenness[i], self.significant_digits))
                    elif player.type is EntityType.non_competitive_player:
                        labels[i] = "" + "\n" + str(round(betweenness[i], self.significant_digits))
                    else:
                        labels[i] = "other_entity"

                sizes = [(10 * c + 1) * 150 for c in list(betweenness.values())]

                graphs.append((temp_graph, labels, sizes))

            # keyboard event handler
            def key_event(e):

                if e.key == "right":
                    self.current_interactive_graph += 1
                elif e.key == "left":
                    self.current_interactive_graph -= 1
                else:
                    return
                self.current_interactive_graph %= len(graphs)

                ax.cla()

                plt.axis([-2, 2, -2, 2])

                curr_pos = self.current_interactive_graph
                nx.draw_networkx(graphs[curr_pos][0], positions, labels=graphs[curr_pos][1], node_color=colors,
                                 node_size=graphs[curr_pos][2],
                                 alpha=self.node_transparency)

                fig.canvas.draw()

            fig = plt.figure()

            fig.canvas.mpl_connect('key_press_event', key_event)
            ax = fig.add_subplot(111)
            plt.axis([-2, 2, -2, 2])

            nx.draw_networkx(graphs[0][0], positions, labels=graphs[0][1], node_color=colors, node_size=graphs[0][2],
                             alpha=self.node_transparency)

            plt.show()

        else:

            plt.ion()

            n = game.rules.nb_players

            positions = {}
            for i in range(n):
                positions[i] = (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))

            colors = ""
            for i in range(n):
                player = game.players[i]
                if player.type is EntityType.competitive_player:
                    colors += self.color_competitive_player
                elif player.type is EntityType.non_competitive_player:
                    colors += self.color_non_competitive_player
                else:
                    colors += self.color_other_entity

            for round_number in range(len(game.history)):

                plt.clf()
                plt.axis([-2, 2, -2, 2])

                temp_graph = nx.Graph()
                temp_graph.add_nodes_from(game.graph.nodes())
                temp_graph.add_edges_from(game.history[round_number])

                labels = {}
                betweenness = nx.betweenness_centrality(temp_graph)
                for i in range(n):
                    player = game.players[i]
                    if player.type is EntityType.competitive_player:
                        labels[i] = game.players[i].name + "\n" + str(round(betweenness[i], self.significant_digits))
                    elif player.type is EntityType.non_competitive_player:
                        labels[i] = "" + "\n" + str(round(betweenness[i], self.significant_digits))
                    else:
                        labels[i] = "other_entity"

                sizes = [(10 * c + 1) * 150 for c in list(betweenness.values())]

                nx.draw_networkx(temp_graph, positions, labels=labels, node_color=colors, node_size=sizes,
                                 alpha=self.node_transparency)
                plt.pause(0.05)

            while True:
                plt.pause(0.05)
