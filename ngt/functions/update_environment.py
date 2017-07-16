from ngt.functions.action import Action
from ngt.rules import ActionSpace, Rules

from typing import Dict, Tuple, Any
from networkx import Graph
Actions = Dict[int, Action]
Reactions = Dict[int, bool]
History = Dict[int, Tuple[Actions, Reactions, Graph]]

update_environment_functions = {}


def update_environment_edge(rules: Rules, graph: Graph, final_actions: Actions) -> None:
    for edge in final_actions.values():
        edge.do(graph)
    return None

update_environment_functions[ActionSpace.edge] = update_environment_edge
