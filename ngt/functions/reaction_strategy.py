"""
Methods related to the concept of player's policy
"""
import networkx as nx
import random
import itertools
from typing import Tuple, Any, Dict
from ngt.rules import Rules, ActionSpace
Actions = Dict[int, Any]
Reactions = Dict[int, bool]

from enum import Enum


"""
Agent's state = history
"""


def inactive(rules: Rules, actions: Actions, agent_state: Any, node_id: int = None) -> None:
    """No action

    Args:
        rules: Rules of the game
        agent_state: Agent representation of the environment
        node_id: Id associated to the player (needed when player is associated to a node in the graph)

    Returns:
        None corresponding to the null action
    """
    return None


class ReactionStrategy(Enum):
    inactive = inactive
