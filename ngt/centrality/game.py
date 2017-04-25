from .rules import Rules
from .player import Player

import pickle
import networkx as nx

class Game:
    def __init__(self):
        self.rules = Rules()
        self.graph = nx.Graph()
        self.players = {}
        self.current_step = 0
        self.history = {}
        self.impossible_edges = []
        self.imposed_edges = []

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
            modified_edge = player.get_action(self, player.node_id)
            if modified_edge is not None:
                modified_edges.add(modified_edge)

        return modified_edges

    def update_env(self, actions):
        """
        Mutates the state of the environment (i.e. the graph) based on the actions performed by the players
        """
        for edge in actions:
            u, v = edge
            if not self.graph.has_edge(*edge) and edge not in self.impossible_edges:
                self.graph.add_edge(u, v)
            elif self.graph.has_edge(*edge) and edge not in self.imposed_edges:
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

    def save(self, filename="history.pickle"):
        # http://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
        game_state = {
        "rules": self.rules,
        "players": self.players,
        "history": self.history,
        "current_step": self.current_step
        }
        with open(filename, 'wb') as handle:
            pickle.dump(game_state, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, filename):
        with open(filename, 'rb') as handle:
            game_state = pickle.load(handle)
            self.rules = game_state["rules"]
            self.players = game_state["players"]
            self.history = game_state["history"]
            self.current_step = game_state["current_step"]
