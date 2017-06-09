"""
Methods related to the concept of player's state (representation of the environment)
"""
from enum import Enum

from typing import Dict, Tuple, Any

from networkx import Graph
from ngt.increment import Increment
Actions = Dict[int, Any]
Reactions = Dict[int, bool]
History = Dict[int, Tuple[Actions, Reactions, Graph]]


def full_history(history: History) -> History:
    return history


def full_graphs(history: History) -> Dict[int, Graph]:
    return {i: increment.graph for i, increment in history.items()}


def last_increment(history: History) -> Increment:
    return history[len(history) - 1]


def last_graph(history: History) -> Graph:
    return history[len(history) - 1].graph


class StateRepresentation(Enum):
    full_history = full_history
    full_graphs = full_graphs
    last_increment = last_increment
    last_graph = last_graph
