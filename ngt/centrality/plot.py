from .entity import EntityType

import networkx as nx

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-poster')


class Plotter:
    def __init__(self):
        self.node_transparency = 0.3
        self.significant_digits = 4
        self.color_competitive_player = "r"
        self.color_non_competitive_player = "b"
        self.color_human = "g"
        self.color_other_entity = "k"
        self.current_interactive_graph = 0  # Allow to navigate through the graphs in interactive mode
        self.labels_interactive_graph = False  # Allow to display the labels in interactive mode

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
            elif player.type is EntityType.human:
                colors += self.color_human
            else:
                colors += self.color_other_entity
        return colors

    def get_graph_labels_sizes(self, game, round_number, node_list=None):
        """
        Compute the labels and sizes of the players according to a given graph state (game + round number)
        :param game: Game, played game
        :param round_number: int, time step/round number of the game
        :param node_list: [int], nodes to be plotted
        :return: tuple containing a dictionary for the labels and an array for the sizes
        """

        current_graph = nx.Graph()
        current_graph.add_nodes_from(game.graph.nodes())
        current_graph.add_edges_from(game.history[round_number])

        labels = {}
        betweenness = nx.betweenness_centrality(current_graph)
        for i in range(game.rules.nb_players):
            player = game.players[i]
            if player.type is EntityType.competitive_player or player.type is EntityType.human:
                labels[i] = "player #" + str(player.node_id) + "\n" +\
                            player.name + "\n" +\
                            str(round(betweenness[i], self.significant_digits))
            elif player.type is EntityType.non_competitive_player:
                labels[i] = "player #" + str(player.node_id) + "\n" +\
                            "" + "\n" +\
                            str(round(betweenness[i], self.significant_digits))
            else:
                labels[i] = "other_entity"

        sizes = [(10 * c + 1) * 300 for c in list(betweenness.values())]

        if node_list is not None:
            current_graph = nx.Graph()
            current_graph.add_nodes_from(node_list)
            current_graph.add_edges_from([edge for edge in game.history[round_number]
                                          if (edge[0] in node_list and edge[1] in node_list)])

            labels = {key: value for (key, value) in labels.items() if key in node_list}

        return current_graph, labels, sizes

    def plot_state(self, game, node_list=None, block=True):
        """
        Plot the current state of a game. Extensive use of NetworkX library, main method used is draw_networkx() and it
        is given various parameters like positions, labels, colors, sizes. The majority of the code here only computes
        those values.
        :param game: Game, current game object
        :param node_list: [int], List of nodes to be plotted
        :param block: boolean, graph stop or not computations
        :return: void
        """
        positions = self.get_positions(game.rules.nb_players)
        colors = self.get_colors(game)
        current_graph, labels, sizes = self.get_graph_labels_sizes(game, len(game.history) - 1, node_list)

        plt.axis([-2, 2, -2, 2])

        nx.draw_networkx(current_graph, positions, labels=labels,
                         node_color=colors, node_size=sizes, alpha=self.node_transparency)
        plt.show(block=block)

    def plot_game(self, game, interactive=False, time_step=0.05, node_list=None):
        """
        Plot a whole game.
        :param game: Game, current game object
        :param interactive: Boolean, if false plot the history of the game, if true allow the user to navigate through
        the state
        :param time_step: int, time step for the non interactive mode
        :param node_list: [int], node to be plotted
        :return: void
        """
        if interactive:

            positions = self.get_positions(game.rules.nb_players)
            colors = self.get_colors(game)
            graphs = [self.get_graph_labels_sizes(game, round_number, node_list)
                      for round_number in range(len(game.history))]

            # keyboard event handler
            def key_event(e):

                if e.key == "right":
                    self.current_interactive_graph += 1
                elif e.key == "left":
                    self.current_interactive_graph -= 1
                elif e.key == "up":
                    self.labels_interactive_graph = True
                elif e.key == "down":
                    self.labels_interactive_graph = False
                else:
                    return
                self.current_interactive_graph %= len(graphs)

                ax.cla()

                plt.axis([-2, 2, -2, 2])

                curr_pos = self.current_interactive_graph

                if self.labels_interactive_graph:
                    nx.draw_networkx(graphs[curr_pos][0], positions, labels=graphs[curr_pos][1], node_color=colors,
                                     node_size=graphs[curr_pos][2], alpha=self.node_transparency)
                else:
                    nx.draw_networkx(graphs[curr_pos][0], positions, node_color=colors, alpha=self.node_transparency)

                fig.canvas.draw()

            fig = plt.figure()

            fig.canvas.mpl_connect('key_press_event', key_event)
            ax = fig.add_subplot(111)
            plt.axis([-2, 2, -2, 2])

            if self.labels_interactive_graph:
                nx.draw_networkx(graphs[0][0], positions, labels=graphs[0][1], node_color=colors,
                                 node_size=graphs[0][2], alpha=self.node_transparency)
            else:
                nx.draw_networkx(graphs[0][0], positions, node_color=colors, alpha=self.node_transparency)

            plt.show()

        else:

            plt.ion()

            positions = self.get_positions(game.rules.nb_players)
            colors = self.get_colors(game)

            for round_number in range(len(game.history)):
                plt.clf()
                plt.axis([-2, 2, -2, 2])
                current_graph, labels, sizes = self.get_graph_labels_sizes(game, round_number, node_list)
                nx.draw_networkx(current_graph, positions, labels=labels, node_color=colors, node_size=sizes,
                                 alpha=self.node_transparency)
                plt.pause(time_step)

            while True:
                plt.pause(0.05)
