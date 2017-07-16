"""Module for generating sets of available actions.
"""

import itertools
import random

from ngt.functions.action import *


# Returns list of EdgeActions
def all_edges(node_list):
    # Removes symmetric edges
    return [EdgeAction(i, j) for i, j in itertools.product(node_list, repeat=2) if i < j]


def all_double_edges(node_list):
    # Removes symmetric edges and symmetric pairs
    return [DoubleEdgeAction(i1, j1, i2, j2) for i1, j1, i2, j2
            in itertools.product(node_list, repeat=4)
            if i1 < j1 and i2 < j2
            and (i1 < i2 or i1 == i2 and j1 < j2)]

def all_assassinations(node_list):
    return [AssassinationAction(i) for i in node_list]

def generate_with_bonus(total_nodes, available_nodes, generate_bonus_actions, bonus_rate):
    all_nodes_list = [i for i in range(total_nodes)]
    random.shuffle(all_nodes_list)
    available_nodes_list = all_nodes_list[:available_nodes]
    actions = []
    actions = actions + all_edges(available_nodes_list)
    if random.random() <= bonus_rate:
        actions += generate_bonus_actions(available_nodes_list)
    return actions


# Tests

def test_all_edges():
    actions = all_edges([2, 4])
    assert len(actions) == 1
    assert repr(actions[0]) == 'EdgeAction(i=2,j=4)'

test_all_edges()


def test_all_double_edges():
    actions = all_double_edges([2, 4, 6])

    assert len(actions) == 3
    assert repr(actions[0]) == 'DoubleEdgeAction(i1=2,j1=4,i2=2,j2=6)'
    assert repr(actions[1]) == 'DoubleEdgeAction(i1=2,j1=4,i2=4,j2=6)'
    assert repr(actions[2]) == 'DoubleEdgeAction(i1=2,j1=6,i2=4,j2=6)'

test_all_double_edges()


def test_all_assassinations():
    actions = all_assassinations([2, 4])

    assert len(actions) == 2
    assert repr(actions[0]) == 'AssassinationAction(i=2)'
    assert repr(actions[1]) == 'AssassinationAction(i=4)'

test_all_assassinations()

def test_generate_with_bonus_zero():
    actions = generate_with_bonus(20, 5, None, 0)

    # 5 nodes yields (5 choose 2) = 10 pairs of nodes
    assert len(actions) == 10

    # Test shuffle. Flaky 1/(20 choose 5) == 1/15504 times (less with ordering).
    actions_for_five_nodes = all_edges(list(range(5)))
    assert [repr(action) for action in actions] != [
    'EdgeAction(i=%d,j=%d)' % (i, j) for i in range(10) for j in range(10) if i < j]


test_generate_with_bonus_zero()


def test_generate_with_bonus_one():
    actions = generate_with_bonus(20, 5, all_assassinations, 1)

    # 10 pairs of nodes plus 5 assassinations
    assert len(actions) == 15

test_generate_with_bonus_one()


def test_generate_with_bonus_half():
    # Simulate at p=0.5 and prove a success and failure can both happen.
    # Flaky 1/2^99 times.
    hit_bonus = False
    missed_bonus = False
    for i in range(100):
        actions = generate_with_bonus(20, 5, all_assassinations, 0.5)
        if len(actions) == 10:
            missed_bonus = True
        if len(actions) == 15:
            hit_bonus = True
        if hit_bonus and missed_bonus:
            # Test passes
            return
    # Test fails
    assert False

test_generate_with_bonus_half()
