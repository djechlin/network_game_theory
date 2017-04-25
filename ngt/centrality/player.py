from .entity import EntityType
from .rules import Rules
from .plot import Plotter

# remove import matplotlib, shouldn't be here
import matplotlib.pyplot as plt

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

    def get_action(self, game, node_id):
        """
        Get the action exercised by the player given the current game history by calling his strategy
        :param game: Game, current game
        :param node_id: int, ID of the current node
        :return: edge to be modified given the strategy of the player and the current history of the game
        (wanted to only consider the current state of the game first but the teacher rightfully indicated that players
        would generally remember the previous states. Anyway, keeping track of the history is more general, allow to
        handle the visualization all at once at the end, and includes the current state, thus we could restrict
        ourselves later.)
        """
        if self.type == EntityType.human:
            print("Here is the current state of the game (history, interactive command to go through history)")
            plotter = Plotter()
            plotter.plot_state(game, block=False)
            # plotter.plot_game(game, block=False, interactive=True)
            u = int(input("Enter the first node id of the edge you want to modify: "))
            v = int(input("Enter the second node id of the edge you want to modify: "))
            print("You decided to build/destroy (use has_edge to choose between create and destroy) the edge (" + str(u) + ", " + str(v) + ")")

            # should be handle by method plot, either automatic or pressing a key if you want plot to stay on screen
            plt.close("all")

            return u, v

        return self.strategy(game.rules.nb_players, node_id, game.history)
