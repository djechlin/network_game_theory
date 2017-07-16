import networkx as nx

from ngt.game import Game
from ngt.rules import ActionSpace
from ngt.player import Player, EntityType
from ngt.plot import plot

from ngt.functions.utility import Utility
from ngt.functions.action import EdgeAction
from ngt.functions.action_strategy import ActionStrategy

if __name__ == '__main__':

    # Create the game

    graph = nx.Graph()
    graph.add_nodes_from(list(range(10)))

    game_info = {
        'nb_players': 10,
        'nb_time_steps': 10,
        'action_space': ActionSpace.edge,
        'impossible_action': set((EdgeAction(0, 1), EdgeAction(1, 0))),
        'graph': graph,
    }

    game = Game(**game_info)

    # Add some players

    player_info = {
        'name': 'Jack',
        'utility_function': Utility.betweenness_centrality,
        'action_strategy': ActionStrategy.myopic_greedy,
        # 'reaction_strategy': None,
    }
    player_info_2 = {
        'name': 'John',
        # 'type': EntityType.human,
        'utility_function': Utility.betweenness_centrality,
        'action_strategy': ActionStrategy.myopic_greedy,
        # 'reaction_strategy': None,
    }

    game.add_player(Player(**player_info))
    # game.add_player(Player(**player_info_2))

    # Play the game

    game.play_game()

    # Save the game

    folder_name = 'my_game'
    game.save(folder_name)

    # Procrastinate

    del game

    # Load the game

    game = Game.load(folder_name)

    # Plot the last state of the game

    plot_args = {
        "node_transparency": 0.3,
        "significant_digits": 4,
        "leader_board_size": 3,
    }

    # still need to clean plot (return ax, handle display externally)
    plot(game, **plot_args)

    # Replay the game

