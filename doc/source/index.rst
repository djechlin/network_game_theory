.. NGT documentation master file, created by
   sphinx-quickstart on Wed May 17 08:02:48 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NGT's documentation!
===============================

NGT (Network Game Theory) is a package to help study game theory applications on dynamic networks. It is highly
dependant on the networkX package. This package aims at providing:

   * an interface to easily simulate classical game theory on dynamic networks situations
   * analytical tools to study networks' metrics evolution through time

Getting started
===============

Install the package by running the following command: pip install ngt

Then, you can create a centrality game where players aim at maximizing their betweenness centrality in the graph
by acting on the graph's edges

.. code-block:: python

    # Import used packages

    import networkx
    import ngt

    # Create the graph that will be used in the game

    graph = networkx.Graph()
    graph.add_nodes_from(list(range(10)))

    # Create the game

    game_info = {
        'nb_players': 10,
        'nb_time_steps': 10,
        'action_space': ActionSpace.edge,
        'impossible_action': set((0, 1)),
        'graph': graph,
    }

    game = Game(**game_info)

    # Add some players

    player_info = {
        'name': 'Leo',
        'utility_function': Utility.betweenness_centrality,
        'action_strategy': ActionStrategy.myopic_greedy,
        # 'reaction_strategy': None,
    }
    player_info_2 = {
        'name': 'Marc',
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

    # Plot the game

    plot_args = {
        "node_transparency": 0.3,
        "significant_digits": 4,
        "leader_board_size": 3,
    }

    # still need to clean plot (return ax, handle display externally)
    # plot(game, **plot_args)

    # Analyze the game

Topical guides
==============

* Centrality maximisation
* Virus/information propagation
* Systemic risk in bank networks

API reference
=============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   rules
   game
   player
