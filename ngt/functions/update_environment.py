from ngt.rules import ActionSpace, Rules

from typing import Dict, Tuple, Any
from networkx import Graph
Actions = Dict[int, Any]
Reactions = Dict[int, bool]
History = Dict[int, Tuple[Actions, Reactions, Graph]]

update_environment_functions = {}


def update_environment_edge(rules: Rules, graph: Graph, final_actions: Actions) -> None:

    for edge in final_actions.values():
        u, v = edge
        if not graph.has_edge(*edge):
            graph.add_edge(u, v)
        elif graph.has_edge(*edge):
            graph.remove_edge(u, v)
    return None

update_environment_functions[ActionSpace.edge] = update_environment_edge
