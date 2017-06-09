import networkx as nx
from ngt.utils import save_object

from typing import Dict, Any
from networkx import Graph
Actions = Dict[int, Any]
Reactions = Dict[int, bool]


class Increment:
    """Class for objects hosting one step history"""
    def __init__(self, actions: Actions = {}, reactions: Reactions = {}, graph: Graph = nx.Graph()):
        """Standard init method

        Args:
            **kwargs: not enforcing input for now
        """
        self.actions = actions
        self.reactions = reactions
        self.graph = graph

    def save(self, folder_name: str, time_step: str) -> None:
        """Save the player object to pickle objects (save Profile, functions...) for persistence

        Args:
            folder_name: Name of the directory holding game pickle objects
            time_step: Id of the player

        Returns:
            None
        """
        save_object(self.actions, folder_name, "increment_" + str(time_step) + "_actions")
        save_object(self.reactions, folder_name, "increment_" + str(time_step) + "_reactions")
        save_object(self.graph, folder_name, "increment_" + str(time_step) + "_graph")

    def __str__(self):
        return str(self.actions)