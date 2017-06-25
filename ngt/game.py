# -*- coding: utf-8 -*-
"""Classes and methods related to the concept of game

Todo:
    * Reaction

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

import networkx as nx

from ngt.rules import ActionSpace, Rules
from ngt.increment import Increment
from ngt.utils import fetch_adequate_function, check_action_type, save_object, load_object, make_sure_path_exists
from ngt.utils import get_players_id, get_increments_id
from ngt.functions.update_environment import update_environment_functions

from typing import Dict, Any
from ngt.player import Player
Actions = Dict[int, Any]
Reactions = Dict[int, bool]


class Game:
    """Class hosting the game logic"""
    def __init__(self, **kwargs):
        """Standard init method

        Args:
            **kwargs: not enforcing input for now
        """
        self.rules = kwargs.get('rules', Rules(**kwargs))
        self.graph = kwargs.get('graph', nx.Graph())
        self.history = kwargs.get('history', {0: Increment(**{'graph': self.graph.copy()})})
        self.players = kwargs.get('players', {})
        self.nodes_players_map = kwargs.get('nodes_players_map', None)
        self.current_time_step = max(self.history.keys(), default=0)

    def add_player(self, player: Player) -> None:
        """Add player to the game

        To do:
            * Input validation

        Args:
            player: Player to be added

        Returns:
            None
        """
        if len(self.players) >= self.rules.nb_players:
            raise Exception("Too many players")

        self.players[len(self.players)] = player

    def play_round(self) -> None:
        """Play one round of the game

        Returns:
            None
        """

        if self.rules.action_space is ActionSpace.edge and len(self.graph.nodes()) < 2:
            raise Exception("Not enough nodes to play a game where the action space is the set of edges")
        elif self.rules.action_space is ActionSpace.node and len(self.graph.nodes()) < 1:
            raise Exception("Not enough nodes to play a game where the action space is the set of nodes")
        elif self.rules.action_space is ActionSpace.boolean and len(self.graph.nodes()) < 1:
            raise Exception("Not enough nodes to play a game where the action space is the acceptance of a policy")
        elif self.rules.action_space is ActionSpace.dynamic_edge and len(self.graph.nodes()) < 2:
            raise Exception("Not enough nodes to play a game where the action space is dynamically computed")

        # Fetch players' actions
        actions = self.fetch_actions()

        # Fetch players' reactions
        reactions = self.fetch_reactions(actions)

        # Compute final actions
        final_actions = self.compute_final_actions(actions, reactions)

        # Update environment
        self.update_environment(final_actions)

        # Update history
        self.current_time_step += 1
        self.history[self.current_time_step] = Increment(actions, reactions, self.graph.copy())

    def play_game(self) -> None:
        """Play an entire game

        Returns:
            None
        """
        while self.current_time_step < self.rules.nb_time_steps:
            self.play_round()

    def fetch_actions(self) -> Actions:
        """Fetch actions chosen by the players given the rules and the history

        Returns:
            Actions chosen by the players
        """
        actions = {}

        for player_id, player in self.players.items():
            action = player.compute_action(self.rules, self.history, player_id)
            action_is_valid = check_action_type(self.rules, action)
            if action_is_valid:
                actions[player_id] = action
            else:
                print(f'Invalid action type by {player} (player with id {player_id})')
        return actions

    def fetch_reactions(self, actions: Actions) -> Reactions:
        """Fetch reactions of the player to the previously chosen actions

        Args:
            actions: Actions previously chosen by the players

        Returns:
            None
        """
        reactions = {}

        for player_id, player in self.players.items():
            reactions[player_id] = player.compute_reaction(self.rules, actions, self.history, player_id)

        return reactions

    def compute_final_actions(self, actions: Actions, reactions: Reactions) -> Actions:
        """Compute the actions that will update the environment given the reactions of the players

        Args:
            actions: Actions chosen by the players
            reactions: Reactions then chosen by the players

        Returns:
            Final actions that will indeed impact the environment
        """
        actions = {i: action
                   for i, action
                   in actions.items()
                   if action not in self.rules.impossible_actions and action is not None}
        return actions

    def update_environment(self, final_actions: Actions) -> None:
        """Update the environment given the players' final actions

        Args:
            final_actions: Players' final actions

        Returns:
            None
        """

        update_function = fetch_adequate_function(self.rules, update_environment_functions)\

        update_function(self.rules, self.graph, final_actions)

    def save(self, folder_name: str) -> None:
        """Save the game object to pickle objects (save Rules, Game, Players, History, current_time_step) for persistence

        Args:
            folder_name: Name of the directory holding game pickle objects

        Returns:
            None
        """

        make_sure_path_exists(folder_name)

        save_object(self.rules, folder_name, "rules")
        save_object(self.nodes_players_map, folder_name, "nodes_players_map")
        save_object(self.current_time_step, folder_name, "current_time_step")
        for id_player, player in self.players.items():
            player.save(folder_name, id_player)
        for time_step, history in self.history.items():
            history.save(folder_name, time_step)

    @staticmethod
    def load(folder_name: str) -> Any:
        """Save the game object to pickle objects (save Rules, Game, Players, History, current_time_step) for persistence

        Args:
           folder_name: Name of the directory holding game pickle objects

        Returns:
            None
        """

        rules = load_object(folder_name, "rules")
        nodes_players_map = load_object(folder_name, "nodes_players_map")
        current_time_step = load_object(folder_name, "current_time_step")

        players = {}
        id_players = get_players_id(folder_name)
        for id_player in id_players:
            action_strategy = load_object(folder_name, f'player_{id_player}_action_strategy')
            reaction_strategy = load_object(folder_name, f'player_{id_player}_reaction_strategy')
            state_representation = load_object(folder_name, f'player_{id_player}_state_representation_function')
            profile = load_object(folder_name, f'player_{id_player}_profile')
            type_pl = load_object(folder_name, f'player_{id_player}_type')
            utility = load_object(folder_name, f'player_{id_player}_utility_function')

            player_info = {
                'type': type_pl,
                'profile': profile,
                'utility': utility,
                'state_representation': state_representation,
                'reaction_strategy': reaction_strategy,
                'action_strategy': action_strategy,
            }

            players[id_player] = Player(**player_info)

        history = {}
        id_increments = get_increments_id(folder_name)
        for id_increment in id_increments:
            increment_actions = load_object(folder_name, f'increment_{id_increment}_actions')
            increment_reactions = load_object(folder_name, f'increment_{id_increment}_reactions')
            increment_graph = load_object(folder_name, f'increment_{id_increment}_graph')

            history[id_increment] = Increment(increment_actions, increment_reactions, increment_graph)

        game_info = {
            'rules': rules,
            'nodes_players_map': nodes_players_map,
            'current_time_step': current_time_step,
            'graph': history[len(history) - 1].graph,
            'players': players,
            'history': history,
        }

        return Game(**game_info)