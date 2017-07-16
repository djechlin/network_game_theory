"""
Methods related to defining available actions for dynamic strategies
"""
import networkx as nx

class Action:
    def __init__(self, **kwargs):
        self.do = kwargs.get('do')
        self.undo = kwargs.get('undo')


def edge(i, j):
    toggle = lambda graph: toggle_edge_(graph, i, j)
    return Action(do=toggle, undo=toggle)


def double_edge(i1, j1, i2, j2):
    def double_toggle(graph):
        toggle_edge_(graph, i1, j1)
        toggle_edge_(graph, i2, j2)
    return Action(do=double_toggle, undo=double_toggle)


def assassination(i):
    neighbors = []
    def do(graph):
        for n in graph.neighbors(i):
            neighbors.append(n)
            graph.remove_edge(i, n)

    def undo(graph):
        for n in neighbors:
            graph.add_edge(i, n)

    return Action(do=do, undo=undo)


def all_edges(node_list):
    return [edge(i, j) for i, j in itertools.product(node_list, repeat=2) if i != j]


def all_double_edges(node_list):
    return [double_edge(i1, j1, i2, j2) for i1, j1, i2, j2
            in itertools.product(node_list, repeat=4)
            if i1 != j1 and i2 != j2 and set([i1, j1]) != set([i2, j2])]

def all_assassinations(node_list):
    return [assassination(i) for i in node_list]


def toggle_edge_(graph, i, j):
    if graph.has_edge(i, j):
        graph.remove_edge(i, j)
    else:
        graph.add_edge(i, j)


# Test

def test_edge():
    graph = nx.empty_graph(2)
    graph.add_edge(0, 1)

    # Test when edge is already present
    removal_action = edge(0, 1)
    removal_action.do(graph)
    assert not graph.has_edge(0, 1)
    removal_action.undo(graph)
    assert graph.has_edge(0, 1)

    # Test when edge is absent
    addition_action = edge(1, 2)
    addition_action.do(graph)
    assert graph.has_edge(1, 2)
    addition_action.undo(graph)
    assert not graph.has_edge(1, 2)

test_edge()


def test_double_edge():
    graph = nx.empty_graph(2);
    graph.add_edge(0, 1)

    action = double_edge(0, 1, 1, 2)

    action.do(graph)
    assert not graph.has_edge(0, 1)
    assert graph.has_edge(1, 2)

    action.undo(graph)
    assert graph.has_edge(0, 1)
    assert not graph.has_edge(1, 2)

test_double_edge()


def test_assassination():
    graph = nx.empty_graph(4)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)

    action = assassination(0)

    action.do(graph)
    assert not graph.has_edge(0, 1)
    assert not graph.has_edge(0, 2)
    assert not graph.has_edge(0, 3)

    action.undo(graph)
    assert graph.has_edge(0, 1)
    assert graph.has_edge(0, 2)
    assert not graph.has_edge(0, 3)


test_assassination()
