import matplotlib.pyplot as plt
import networkx as nx
import math
from random import randint, random, shuffle
from enum import Enum
import itertools
from approximate_betweenness import approximate_betweenness_centrality
import pickle


class Rules:
    def __init__(self):
        self.nb_players = 10
        self.nb_max_step = 10


class EntityType(Enum):
    competitive_player = 1
    non_competitive_player = 2
    other_entity = 3


class Player:
    def __init__(self):
        self.rules = Rules()
        self._type = EntityType.non_competitive_player
        self.node_id = -1
        self.name = "John"
        self.strategy = lambda nb_nodes, node_id, history: None

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    def get_action(self, nb_nodes, node_id, history):
        """
        Get the action exercised by the player given the current game history by calling his strategy
        :param nb_nodes: int, number of nodes in the graph
        :param node_id: int, ID of the current node
        :param history: Dict(List(edges)), history of the game (all the states of the graph up to the present moment).
        One state is a list of edges, the history uses a dictionary where the keys represent the time of the state.
        :return: edge to be modified given the strategy of the player and the current history of the game
        (wanted to only consider the current state of the game first but the teacher rightfully indicated that players
        would generally remember the previous states. Anyway, keeping track of the history is more general, allow to
        handle the visualization all at once at the end, and includes the current state, thus we could restrict
        ourselves later.)
        """
        return self.strategy(nb_nodes, node_id, history)


class StrategyBuilder:
    """
    The strategies could be defined as static from a pure code point of view but we don't define them this way to
    ensure that each player instantiate a strategy object so that they don't share the exact same strategy in memory.
    """
    @staticmethod
    def get_random_egoist_edge(nb_nodes, node_id):
        """
        Helper function that returns an edge between node_id and a node chosen uniformly at random in the set of
        remaining nodes
        :param nb_nodes: Number of players
        :param node_id: Id of the node calling the function
        :return: tuple (node_id, id of another random node)
        """
        other_nodes = list(range(nb_nodes))
        other_nodes.remove(node_id)
        return node_id, other_nodes[randint(0, nb_nodes - 2)]

    def get_inactive_strategy(self):
        """
        Define and return the inactive strategy
        :return: function that returns None when being called (player won't do anything)
        """
        def inactive_strategy(nb_nodes, node_id, history):
            return None
        return inactive_strategy

    def get_random_strategy(self):
        """
        Define and return the random strategy
        :return: function that returns a random action (random edge) knowing that a looping edge (u == v) is not
        allowed in the game and is therefore replaced by None
        """
        def random_strategy(nb_nodes, node_id, history):
            u, v = randint(0, nb_nodes - 1), randint(0, nb_nodes - 1)
            if u == v:
                return None
            else:
                return u, v
        return random_strategy

    def get_random_egoist_strategy(self):
        """
        Define and return the random egoist strategy (modified edge is random but has the current node as one end)
        :return: function that returns a random action (random edge) knowing that a looping edge (u == v) is not
        allowed in the game and is therefore replaced by None
        """
        def random_egoist_strategy(nb_nodes, node_id, history):
            return self.get_random_egoist_edge(nb_nodes, node_id)
        return random_egoist_strategy

    def get_greedy_strategy(self):
        """
        Define and return the greedy strategy (myopic, only based on the current state and best current action)
        :return: function that returns the best myopic ation given the current state
        """
        def greedy_strategy(nb_nodes, node_id, history):

            # if graph is empty, return random egoist
            if len(history[len(history) - 1]) == 0:
                return self.get_random_egoist_edge(nb_nodes, node_id)

            # build graph related to the current state
            graph = nx.Graph()
            graph.add_nodes_from(list(range(nb_nodes)))
            graph.add_edges_from(history[len(history) - 1])

            # initialize the best current action
            best_u, best_v, best_bet = 0, 0, nx.betweenness_centrality(graph)[node_id]

            # all possible edges:
            possible_edges = list(itertools.combinations(list(range(nb_nodes)), 2))
            # iterate through all possible action (possible edge) and keep track of the best choice
            for i, j in possible_edges:
                if graph.has_edge(i, j):
                    graph.remove_edge(i, j)
                    new_bet = nx.betweenness_centrality(graph)[node_id]
                    if new_bet > best_bet:
                        best_u, best_v, best_bet = i, j, new_bet
                    graph.add_edge(i, j)
                elif i == node_id or j == node_id:
                    # a greedy player would only consider adding edges adjacent to itself 
                    graph.add_edge(i, j)

                    new_bet = nx.betweenness_centrality(graph)[node_id]
                    if new_bet > best_bet:
                        best_u, best_v, best_bet = i, j, new_bet

                    graph.remove_edge(i, j)

            if best_u == best_v:
                return None
            else:
                return best_u, best_v

        return greedy_strategy

    def get_approx_greedy_strategy(self, EPSILON=.1, DELTA=.05):
        """
        Define and return the greedy strategy (myopic, only based on the current state and best current action)
        :return: function that returns the best myopic ation given the current state
        """
        def approx_greedy_strategy(nb_nodes, node_id, history, EPSILON=EPSILON, DELTA=DELTA):
            # if graph is empty, return random egoist
            EPSILON = EPSILON
            DELTA = DELTA
            if len(history[len(history) - 1]) == 0:
                return self.get_random_egoist_edge(nb_nodes, node_id)

            # build graph related to the current state
            graph = nx.Graph()
            graph.add_nodes_from(list(range(nb_nodes)))
            graph.add_edges_from(history[len(history) - 1])

            # initialize the best current action
            best_u, best_v, best_bet = 0, 0, approximate_betweenness_centrality(graph, eps=EPSILON, delta=DELTA)[node_id]

            # all possible edges:
            possible_edges = list(itertools.combinations(list(range(nb_nodes)), 2))
            # iterate through all possible action (possible edge) and keep track of the best choice
            for i, j in possible_edges:
                if graph.has_edge(i, j):
                    graph.remove_edge(i, j)
                    new_bet = approximate_betweenness_centrality(graph, eps=EPSILON, delta=DELTA)[node_id]
                    if new_bet > best_bet:
                        best_u, best_v, best_bet = i, j, new_bet
                    graph.add_edge(i, j)
                elif i == node_id or j == node_id:
                    # a greedy player would only consider adding edges adjacent to itself 
                    graph.add_edge(i, j)

                    new_bet = approximate_betweenness_centrality(graph, eps=EPSILON, delta=DELTA)[node_id]
                    if new_bet > best_bet:
                        best_u, best_v, best_bet = i, j, new_bet

                    graph.remove_edge(i, j)

            if best_u == best_v:
                return None
            else:
                return best_u, best_v

        return approx_greedy_strategy


class Game:
    def __init__(self, rules=Rules()):
        self.rules = rules
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

    def get_actions(self):
        """
        Returns the actions for each player's embedded strategy
        """
        modified_edges = set()

        for node_id, player in self.players.items():
            modified_edge = player.get_action(self.rules.nb_players, player.node_id, self.history)
            if modified_edge is not None:
                modified_edges.add(modified_edge)

        return modified_edges

    def update_env(self, actions):
        """
        Mutates the state of the environment (i.e. the graph) based on the actions performed by the players
        """
        for edge in actions:
            if edge == None:
                pass
            else: 
                u, v = edge
                if not self.graph.has_edge(*edge):
                    self.graph.add_edge(u, v)
                else:
                    self.graph.remove_edge(u, v)

    def play_round(self, actions=False):
        """
        Play one round of the game. For now, if two players are acting on the same edge, the logical OR component
        is adopted (meaning if two players want to destroy the same edge, it will get destroyed).
        No notion of edge strength and cumulative nodes strength yet
        :return: void
        """
        if not actions:
            actions = self.get_actions()

        self.update_env(actions)

        self.current_step += 1

        self.history[self.current_step] = self.graph.edges()

    def play_game(self):
        """
        Play the entire game according to the given rules (total number of steps in a game)
        :return: void
        """
        while self.current_step < self.rules.nb_max_step:
            self.play_round()

    def reset(self):
        """
        Reset the game
        """
        self.graph = nx.Graph()
        self.players = {}
        self.current_step = 0
        self.history = {}
        self.initialize_graph()


    def save(self, filename="history.pickle"):
        # http://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
        game_state = {
        "rules": self.rules,
        "history": self.history,
        "current_step": self.current_step
        }
        with open(filename, 'wb') as handle:
            pickle.dump(game_state, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, filename):
        with open(filename, 'rb') as handle:
            game_state = pickle.load(handle)
            self.rules = game_state["rules"]
            self.history = game_state["history"]
            self.current_step = game_state["current_step"]

class Plotter:
    def __init__(self):
        self.node_transparency = 0.3
        self.significant_digits = 4
        self.color_competitive_player = "r"
        self.color_non_competitive_player = "b"
        self.color_other_entity = "g"
        self.current_interactive_graph = 0  # Allow to navigate through the graphs in interactive mode

    @staticmethod
    def get_positions(nb_players):
        """
        Compute the positions of the players so that they are fixed when visualizing the evolution of the game
        :param nb_players: int, number of players in the game
        :return: dictionary of (x,y) coordinate tuple
        """
        positions = {}
        for i in range(nb_players):
            positions[i] = (math.cos(2 * math.pi * i / nb_players), math.sin(2 * math.pi * i / nb_players))
        return positions

    def get_colors(self, game):
        """
        Compute the colors of the players according to their entity type to be able to easily differentiate them
        :param game: Game, played game
        :return: string of color initials
        """
        colors = ""
        for i in range(game.rules.nb_players):
            player = game.players[i]
            if player.type is EntityType.competitive_player:
                colors += self.color_competitive_player
            elif player.type is EntityType.non_competitive_player:
                colors += self.color_non_competitive_player
            else:
                colors += self.color_other_entity
        return colors

    def get_graph_labels_sizes(self, game, round_number):
        """
        Compute the labels and sizes of the players according to a given graph state (game + round number)
        :param game: Game, played game
        :param nb_players: int, number of players in the game
        :param round_number: int, time step/round number of the game
        :return: tuple containing a dictionary for the labels and an array for the sizes
        """
        current_graph = nx.Graph()
        current_graph.add_nodes_from(game.graph.nodes())
        current_graph.add_edges_from(game.history[round_number])

        labels = {}
        betweenness = nx.betweenness_centrality(current_graph)
        for i in range(game.rules.nb_players):
            player = game.players[i]
            if player.type is EntityType.competitive_player:
                labels[i] = game.players[i].name + "\n" + str(round(betweenness[i], self.significant_digits))
            elif player.type is EntityType.non_competitive_player:
                labels[i] = "" + "\n" + str(round(betweenness[i], self.significant_digits))
            else:
                labels[i] = "other_entity"

        sizes = [(10 * c + 1) * 150 for c in list(betweenness.values())]

        return current_graph, labels, sizes

    def plot_state(self, game):
        """
        Plot the current state of a game. Extensive use of NetworkX library, main method used is draw_networkx() and it
        is given various parameters like positions, labels, colors, sizes. The majority of the code here only computes
        those values.
        :param game: Game, current game object
        :return: void
        """
        positions = self.get_positions(game.rules.nb_players)
        colors = self.get_colors(game)
        current_graph, labels, sizes = self.get_graph_labels_sizes(game, len(game.history) - 1)

        nx.draw_networkx(current_graph, positions, labels=labels,
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

            positions = self.get_positions(game.rules.nb_players)
            colors = self.get_colors(game)
            graphs = [self.get_graph_labels_sizes(game, round_number) for round_number in range(len(game.history))]

            # graphs = []
            # for round_number in range(len(game.history)):
            #     current_graph, labels, sizes = self.get_current_graph_labels_sizes(game, round_number)
            #     graphs.append((current_graph, labels, sizes))

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
                                 node_size=graphs[curr_pos][2], alpha=self.node_transparency)

                fig.canvas.draw()

            fig = plt.figure()

            fig.canvas.mpl_connect('key_press_event', key_event)
            ax = fig.add_subplot(111)
            plt.axis([-2, 2, -2, 2])

            nx.draw_networkx(graphs[0][0], positions, labels=graphs[0][1], node_color=colors,
                             node_size=graphs[0][2], alpha=self.node_transparency)

            plt.show()

        else:

            plt.ion()

            positions = self.get_positions(game.rules.nb_players)
            colors = self.get_colors(game)

            for round_number in range(len(game.history)):
                plt.clf()
                plt.axis([-2, 2, -2, 2])
                current_graph, labels, sizes = self.get_graph_labels_sizes(game, round_number)
                nx.draw_networkx(current_graph, positions, labels=labels, node_color=colors, node_size=sizes,
                                 alpha=self.node_transparency)
                plt.pause(0.05)

            while True:
                plt.pause(0.05)
