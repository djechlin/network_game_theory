"""Module hosting everything related to the rules of a game

Instances of those classes define the action space, the number of players and number of time steps in a game

"""
from enum import Enum


class ActionSpace(Enum):
    edge = 1
    node = 2
    boolean = 3
    dynamic_edge = 4

class Rules:
    def __init__(self, **kwargs):
        self.nb_players = kwargs.get('nb_players', 10)
        self.nb_time_steps = kwargs.get('nb_time_steps', 10)
        self.impossible_actions = kwargs.get('impossible_actions', set())
        self.action_space = kwargs.get('action_space', ActionSpace.edge)
        self.generate_dynamic_actions = kwargs.get('generate_dynamic_actions', None)


    def is_impossible(self, action):
        return repr(action) in [repr(impossible_action)
                                for impossible_action in self.impossible_actions]
