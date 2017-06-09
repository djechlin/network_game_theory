.. NGT documentation master file, created by
   sphinx-quickstart on Wed May 17 08:02:48 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NGT's documentation!
===============================

NGT (Network Game Theory) is a package to help study game theory applications on dynamic networks. It is highly
dependant on the networkX package. This package aims at providing:

   * an interface to easily simulate classical game theory on dynamic networks situations
   * analytical tools to study networks's metrics evolution through time

Getting started
===============

Install the package by running the following command: pip install ngt

Then, you will create a centrality game where players act on graph edges

.. code-block:: python

   """
   Create rules and game
   """

   rules = ngt.Rules()
   rules.nb_max_step = 20
   rules.nb_players = 10

   game = ngt.Game()
   game.rules = rules

   """
   Create some players and add them to the game
   After having initialized the graph so that
   every player receives an id, add some impossible edges
   """

   player1 = Player(rules=rules,
                    type=EntityType.competitive_player,
                    name="Greedy1",
                    strategy_type=Strategy.greedy)
   player2 = Player(rules=rules,
                    type=EntityType.human,
                    name="Human1")

   game.add_player(player1)
   game.add_player(player2)

   game.initialize_graph()

   game.impossible_edges = [
       (player1.node_id, player2.node_id)
   ]

   """
   Play the game
   """

   game.play_game(True)

   """
   Save the game
   """

   # game.save(filename="game.pkl")

   """
   Load the game
   """

   # game = Game()
   # game.load("game.pkl")

   """
   Replay the game
   """

   plotter = Plotter()
   # plotter.plot_state(game)
   plotter.plot_game(game, interactive=False, leader_board=True, time_step=0.01)


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

   algorithms
   centrality