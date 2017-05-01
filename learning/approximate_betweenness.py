import numpy as np
import networkx as nx
import random

def getVertexDiameter(G):
    """
    This is guaranteed to be between VD(G) and 2*VD(G)
    """
    v = random.choice(G.nodes())
    paths = nx.single_source_shortest_path_length(G, v)
    # y take VD(G) to be the sum of the lengths of the two shortest paths with maximum size
    return sum(sorted(paths.values())[-3:-1])

def getSampleSize(VD, eps=.05, delta=.05, c=.5):
    """
    With probability at least 1 − δ, all the approximations computed by the algorithm are within ε
    from their real value
    https://pdfs.semanticscholar.org/213c/7f8e9a8a046020ebfa2a7aaa194b3c05a87a.pdf
    
    By default, this returns sample size needed for 5% error with at least 95% probability
    """
    r = None
    if VD <= 2:
        VD = 3
    while r is None:
        try:
            r = (c / eps**2) * (np.floor(np.log2(VD - 2)) + np.log(1/delta))
        except:
            pass
    return r

def sampleUniformVertexPair(G):
    """
    Returns a random pair of nodes (no self-loops)
    """
    return np.random.choice(G.nodes(), 2, replace=False)

def computeAllShortestPaths(G, u, v):
    """
    Returns a list of lists (each sublist is a shortest path from u to v)
    """
    try:
        S = list(nx.all_shortest_paths(G,source=u,target=v))
    except:
        S = {}
    return S


def getShortestSubPaths(paths, t):
    return [path[:-1] for path in paths if t in path]
    

def pathCount(paths, t):
    return len([path for path in paths if t in path])

def approximate_betweenness_centrality(G, eps=.05, delta=.05, c=.5):
    """
    Computes the approximate betweenness centrality for the nodes in graph G
    within epsilon error with probability at least 1 - δ.
    https://pdfs.semanticscholar.org/213c/7f8e9a8a046020ebfa2a7aaa194b3c05a87a.pdf
    
    Fast Approximation of Betweenness Centrality through Sampling,
    Matteo Riondato and Evgenios M. Kornaropoulos
    """
    b = dict.fromkeys(G, 0.0)  # b[v]=0 for v in G
    # approximate ~ guaranteed VD <= approx <= 2*VD
    VD = getVertexDiameter(G)
    r = None
    while r is None:
        # if VD <= 2, there are dragons
        try:
            r = int(getSampleSize(VD, eps=eps, delta=delta, c=1))
        except:
            pass
    for i in range(r):
        u, v = sampleUniformVertexPair(G)
        S = computeAllShortestPaths(G, u, v)
        if S:
            # Random path sampling and estimation update
            t = v
            while t != u:
                z_candidates = []
                S_t = getShortestSubPaths(S, t)
                sigma_ut = len(S_t)
                z_probs = []
                for path in S_t:
                    # add immediate predecessors to be candidates for z
                    predecessor = path[-1]
                    z_candidates.append(predecessor)
                    # the number of shortest paths from u to candidate z
                    z_probs.append(pathCount(S_t, predecessor) / sigma_ut)
                # normalize probability
                z_probs = z_probs / np.sum(z_probs)
                # choose a z with weighted probability
                z = np.random.choice(z_candidates, 1, p=z_probs)[0]
                if z != u:
                    # if we haven't backed up all the way, update b(z)
                    b[z] += 1 / r
                t = z
                S = S_t
    return b