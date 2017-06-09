# -*- coding: utf-8 -*-
"""Classes and methods related to the concept of players/agents/entities.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

.. _Reinforcement Learning Theory:
   http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching.html

"""
from enum import Enum

from ngt.utils import fetch_adequate_function, check_action_type, save_object, make_sure_path_exists
from ngt.rules import ActionSpace

from ngt.functions.action_strategy import ActionStrategy
from ngt.functions.reaction_strategy import ReactionStrategy
from ngt.functions.state_representation import StateRepresentation
from ngt.functions.utility import Utility

from typing import Dict, Tuple, Any

from networkx import Graph
from ngt.rules import Rules
Actions = Dict[int, Any]
Reactions = Dict[int, bool]
History = Dict[int, Tuple[Actions, Reactions, Graph]]


class EntityType(Enum):
    bot = 1
    human = 2


class Profile:
    """Class related to a player's metadata"""
    def __init__(self, **kwargs):
        """Standard init method

        :param kwargs: don't want to enforce any arg for now
        """
        self.name = kwargs.get('name', "Unnamed")


class Player:
    """Class related to a player"""
    def __init__(self, **kwargs):
        """Standard init method

        :param kwargs: don't want to enforce any arg for now
        """
        self.type = kwargs.get('type', EntityType.bot)
        self.profile = kwargs.get('profile', Profile(**kwargs))
        self.state_representation_function = kwargs.get('state_representation_function',
                                                        StateRepresentation.full_history)
        self.utility_function = kwargs.get('utility_function', Utility.betweenness_centrality)
        self.action_strategy = kwargs.get('action_strategy', ActionStrategy.myopic_greedy)
        self.reaction_strategy = kwargs.get('reaction_strategy', ReactionStrategy.inactive)

    def __str__(self):
        return self.profile.name

    def compute_action(self, rules: Rules, history: History, player_id: int) -> Any:
        """Compute the action chosen by the player given the history

        Args:
            rules: Rules of the game
            history: History of the game
            player_id: Id of the player (needed when player associated to a node)

        Returns:
            Action
        """

        agent_state = self.state_representation_function(history)

        agent_action = self.get_action(rules, agent_state, player_id)

        return agent_action

    def compute_reaction(self, rules: Rules, actions: Actions, history: History, player_id: int) -> Any:
        """Compute the reaction chosen by the player given the actions of other players

        The concept of reaction is rarely raised but still useful in the network setting
        where one could consider the creation of an edge requires a bilateral agreement from
        both nodes.

        Args:
            rules: Rules of the game
            actions: Actions chosen by the players
            history: History of the game
            player_id: Id of the player (needed when player associated to a node)

        Returns:
            Action
        """

        agent_state = self.state_representation_function(history)

        agent_reaction = self.get_reaction(rules, actions, agent_state, player_id)

        return agent_reaction

    def get_action(self, rules: Rules, agent_state: Any, player_id) -> Any:
        """Compute the action chosen by the player given his representation of the environment (Agent's state)

        Args:
            rules: Rules of the game
            agent_state: Environment as perceived by the player
            player_id: Id of the player (needed when player associated to a node)

        Returns:
            Player action (type depend on action space (edge, node, bool, ...))
        """

        if self.type == EntityType.human:
            # plotter = Plotter()
            # plotter.plot_state(game, block=False)
            # # plotter.plot_game(game, block=False, interactive=True)

            if rules.action_space is ActionSpace.edge:

                u = int(input("Enter the first node id of the edge you want to modify: "))
                v = int(input("Enter the second node id of the edge you want to modify: "))
                print("You decided to build/destroy (use has_edge to choose between create and destroy) the edge (" + str(u) + ", " + str(v) + ")")
                return u, v



            # should be handle by method plot, either automatic or pressing a key if you want plot to stay on screen
            # plt.close("all")


        return self.action_strategy(rules, agent_state, self.utility_function, player_id)

    def get_reaction(self, rules: Rules, actions: Actions, agent_state: Any, player_id) -> bool:
        """Compute the reaction chosen by the player given his representation of the environment (Agent's state)

        Args:
            rules: Rules of the game
            actions: Actions chosen by the players
            agent_state: Environment as perceived by the player
            player_id: Id of the player (needed when player associated to a node)

        Returns:
            Player reaction
        """

        # if self.type == EntityType.human:
        #     plotter = Plotter()
        #     plotter.plot_state(game, block=False)
        #     # plotter.plot_game(game, block=False, interactive=True)
        #     u = int(input("Enter the first node id of the edge you want to modify: "))
        #     v = int(input("Enter the second node id of the edge you want to modify: "))
        #     print("You decided to build/destroy (use has_edge to choose between create and destroy) the edge (" + str(u) + ", " + str(v) + ")")
        #
        #     # should be handle by method plot, either automatic or pressing a key if you want plot to stay on screen
        #     plt.close("all")
        #
        #     return u, v

        return self.reaction_strategy(rules, actions, agent_state, player_id)

    def save(self, folder_name: str, id_player: str) -> None:
        """Save the player object to pickle objects (save Profile, functions...) for persistence

        Args:
            folder_name: Name of the directory holding game pickle objects
            id_player: Id of the player

        Returns:
            None
        """

        save_object(self.type, folder_name, "player_" + str(id_player) + "_type")
        save_object(self.profile, folder_name, "player_" + str(id_player) + "_profile")
        save_object(self.state_representation_function, folder_name, "player_" + str(id_player)
                    + "_state_representation_function")
        save_object(self.action_strategy, folder_name, "player_" + str(id_player) + "_action_strategy")
        save_object(self.reaction_strategy, folder_name, "player_" + str(id_player) + "_reaction_strategy")
        save_object(self.utility_function, folder_name, "player_" + str(id_player) + "_utility_function")
