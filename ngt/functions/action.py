"""
Methods related to defining available actions for dynamic strategies
"""
import networkx as nx

class Action:
    def do(self):
        pass


    def undo(self):
        pass


class EdgeAction(Action):

    def __init__(self, i, j):
        self.i = i
        self.j = j

    def do(self, graph):
        toggle_edge_(graph, self.i, self.j)

    def undo(self, graph):
        toggle_edge_(graph, self.i, self.j)

    def __repr__(self):
        return 'EdgeAction(i=%d,j=%d)' % (self.i, self.j)

class DoubleEdgeAction(Action):

    def __init__(self, i1, j1, i2, j2):
        self.i1 = i1
        self.j1 = j1
        self.i2 = i2
        self.j2 = j2

    def do(self, graph):
        self.double_toggle_(graph)

    def undo(self, graph):
        self.double_toggle_(graph)

    def __repr__(self):
        return 'DoubleEdgeAction(i1=%d,j1=%d,i2=%d,j2=%d)' % (self.i1, self.j1, self.i2, self.j2)

    def double_toggle_(self, graph):
        toggle_edge_(graph, self.i1, self.j1)
        toggle_edge_(graph, self.i2, self.j2)


class AssassinationAction(Action):

    def __init__(self, i):
        self.neighbors = []
        self.i = i

    def do(self, graph):
        for n in graph.neighbors(self.i):
            self.neighbors.append(n)
            graph.remove_edge(self.i, n)

    def undo(self, graph):
        for n in self.neighbors:
            graph.add_edge(self.i, n)

    def __repr__(self):
        return 'AssassinationAction(i=%d)' % (self.i,)


def all_edges(node_list):
    return [EdgeAction(i, j) for i, j in itertools.product(node_list, repeat=2) if i != j]


def all_double_edges(node_list):
    return [DoubleEdgeAction(i1, j1, i2, j2) for i1, j1, i2, j2
            in itertools.product(node_list, repeat=4)
            if i1 != j1 and i2 != j2 and set([i1, j1]) != set([i2, j2])]

def all_assassinations(node_list):
    return [AssassinationAction(i) for i in node_list]


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
    removal_action = EdgeAction(0, 1)
    removal_action.do(graph)
    assert not graph.has_edge(0, 1)
    removal_action.undo(graph)
    assert graph.has_edge(0, 1)

    # Test when edge is absent
    addition_action = EdgeAction(1, 2)
    addition_action.do(graph)
    assert graph.has_edge(1, 2)
    addition_action.undo(graph)
    assert not graph.has_edge(1, 2)

    # Test repr
    assert repr(removal_action) == 'EdgeAction(i=0,j=1)'

test_edge()


def test_double_edge():
    graph = nx.empty_graph(2);
    graph.add_edge(0, 1)

    action = DoubleEdgeAction(0, 1, 1, 2)

    action.do(graph)
    assert not graph.has_edge(0, 1)
    assert graph.has_edge(1, 2)

    action.undo(graph)
    assert graph.has_edge(0, 1)
    assert not graph.has_edge(1, 2)

    # Test repr
    assert repr(action) == 'DoubleEdgeAction(i1=0,j1=1,i2=1,j2=2)'

test_double_edge()


def test_assassination():
    graph = nx.empty_graph(4)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)

    action = AssassinationAction(0)

    action.do(graph)
    assert not graph.has_edge(0, 1)
    assert not graph.has_edge(0, 2)
    assert not graph.has_edge(0, 3)

    action.undo(graph)
    assert graph.has_edge(0, 1)
    assert graph.has_edge(0, 2)
    assert not graph.has_edge(0, 3)

    # Test repr
    assert repr(action) == 'AssassinationAction(i=0)'


test_assassination()