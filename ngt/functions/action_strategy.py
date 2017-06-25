"""
Methods related to the concept of player's policy
"""
import networkx as nx
import random
import itertools
from typing import Tuple, Any
from ngt.rules import Rules, ActionSpace
from ngt.functions.utility import Utility

from enum import Enum


"""
Agent's state = history
"""


def inactive(rules: Rules, agent_state: Any, node_id: int = None) -> None:
    """No action

    Args:
        rules: Rules of the game
        agent_state: Agent representation of the environment
        node_id: Id associated to the player (needed when player is associated to a node in the graph)

    Returns:
        None corresponding to the null action
    """
    return None


def random_random(rules: Rules, agent_state: Any, node_id: int = None) -> Any:
    """Randomly pick an action (beware name conflict with random package)

    Args:
        rules: Rules of the game
        agent_state: Agent representation of the environment
        node_id: Id associated to the player (needed when player is associated to a node in the graph)

    Returns:
        Action that could be of any type. Type given by the rules.
    """

    if rules.action_space is ActionSpace.edge:

        # Myopic, keep only last graph from history
        graph = agent_state[len(agent_state) - 1].graph

        # Get list of nodes and pick one randomly (exclude node associated to player first)
        nodes = graph.nodes()

        if node_id is not None:
            nodes.remove(node_id)

        u = random.choice(nodes)

        u, v = random.choice(nodes), random.choice(nodes)
        if u == v:
            return None
        else:
            return u, v

    elif rules.action_space is ActionSpace.node:
        pass
    elif rules.action_space is ActionSpace.boolean:
        pass
    elif rules.action_space is ActionSpace.dynamic_edge:
        pass


def random_egoist(rules: Rules, agent_state: Any, node_id: int = None) -> Any:
    """Randomly pick an action, with egoistic motivation (eg: edge creation with himself)

    It is assumed agents state is equal to the history, don't really know how to cleanly
    handle (without billions of conditional statements) the various agent_state types that could
    exist. For know, have to code method accordingly.

    Args:
        rules: Rules of the game
        agent_state: Agent representation of the environment
        node_id: Id associated to the player (needed when player is associated to a node in the graph)

    Returns:
        Action that could be of any type. Type given by the rules.
    """

    if rules.action_space is ActionSpace.edge:

        # Myopic, keep only last graph from history
        graph = agent_state[len(agent_state) - 1].graph

        # Get list of nodes and pick one randomly (exclude node associated to player first)
        nodes = graph.nodes()

        if node_id is not None:
            nodes.remove(node_id)

        u = random.choice(nodes)

        return node_id, u

    elif rules.action_space is ActionSpace.node:
        pass
    elif rules.action_space is ActionSpace.boolean:
        pass
    elif rules.action_space is ActionSpace.dynamic_edge:
        pass


def follower(rules: Rules, agent_state: Any, node_id: int = None) -> Any:

    if rules.action_space is ActionSpace.edge:

        # Myopic, keep only last graph from history
        graph = agent_state[len(agent_state) - 1].graph

        # Find the best players and order them in decreasing order
        inverse = [(value, key) for key, value in nx.betweenness_centrality(graph).items()]
        sorted(inverse, reverse=True)

        for i in range(len(inverse)):
            if not graph.has_edge(node_id, inverse[i][1]):
                return node_id, inverse[i][1]

        return None

    elif rules.action_space is ActionSpace.node:
        pass
    elif rules.action_space is ActionSpace.boolean:
        pass
    elif rules.action_space is ActionSpace.dynamic_edge:
        pass


def myopic_greedy(rules: Rules, agent_state: Any, utility: Utility, node_id: int = None) -> Any:

    if rules.action_space is ActionSpace.edge:

        # myopic, keep only last graph from history
        graph = agent_state[len(agent_state) - 1].graph

        # if graph is empty, return random egoist
        if len(graph.edges()) == 0:
            return random_egoist(rules, agent_state, node_id)

        # initialize the best current action
        best_u, best_v, best_bet = 0, 0, utility(graph, node_id)

        # create the list of possible edges
        edges_combination = list(itertools.combinations(range(len(graph.nodes())), r=2))

        # iterate through all possible action and keep track of the best choice
        for i, j in edges_combination:
            if (i, j) in rules.impossible_actions or (j, i) in rules.impossible_actions:
                continue

            if graph.has_edge(i, j) or graph.has_edge(j, i):
                graph.remove_edge(i, j)

                new_bet = utility(graph, node_id)

                if new_bet > best_bet:
                    best_u, best_v, best_bet = i, j, new_bet

                graph.add_edge(i, j)

            else:
                graph.add_edge(i, j)

                new_bet = utility(graph, node_id)
                if new_bet > best_bet:
                    best_u, best_v, best_bet = i, j, new_bet

                graph.remove_edge(i, j)

        if best_u == best_v:
            return None
        else:
            return best_u, best_v

    elif rules.action_space is ActionSpace.node:
        pass
    elif rules.action_space is ActionSpace.boolean:
        pass
    elif rules.action_space is ActionSpace.dynamic_edge:
        pass


class ActionStrategy(Enum):
    inactive = inactive
    random_random = random_random
    random_egoist = random_egoist
    myopic_greedy = myopic_greedy
