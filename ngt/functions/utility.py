"""
Methods related to the concept of player's utility
"""
from enum import Enum
import networkx as nx
from typing import List, Tuple
from networkx import Graph

"""
Utility based on micro measures
"""


def betweenness_centrality(graph: Graph, node_id: int) -> float:
    # Bias players to prefer being connected to anything over nothing
    if graph.degree(node_id) == 0:
        return -.0001
    return nx.betweenness_centrality(graph)[node_id]


"""
Utility based on macro measures
"""


def average_clustering(graph: Graph) -> float:
    return nx.average_clustering(graph)


class Utility(Enum):
    betweenness_centrality = betweenness_centrality
    average_clustering = average_clustering
