"""
apollonian 网络
无标度、小世界、电导

聚类系数大、最短路径随着站点数目对数增长，





Zhou T, Yan G, Zhou P L, et al. Random apollonian networks[J]. arXiv preprint cond-mat/0409414, 2004.
Andrade R F S, Herrmann H J. Magnetic models on Apollonian networks[J]. Physical Review E, 2005, 71(5): 056131.
Andrade Jr J S, Herrmann H J, Andrade R F S, et al. Apollonian networks: Simultaneously scale-free, small world, Euclidean, space filling, and with matching graphs[J]. Physical review letters, 2005, 94(1): 018702.

"""
import networkx as nx
from matplotlib import pyplot as plt
from collections import Counter

def _triangles_and_degree_iter(G, nodes=None):
    """ Return an iterator of (node, degree, triangles, generalized degree).

    This double counts triangles so you may want to divide by 2.
    See degree(), triangles() and generalized_degree() for definitions
    and details.

    """
    if nodes is None:
        nodes_nbrs = G.adj.items()
    else:
        nodes_nbrs = ((n, G[n]) for n in G.nbunch_iter(nodes))
    for v, v_nbrs in nodes_nbrs:
        vs = set(v_nbrs) - {v}
        gen_degree = Counter(len(vs & (set(G[w]) - {w})) for w in vs)
        ntriangles = sum(k * val for k, val in gen_degree.items())
        yield (v, len(vs), ntriangles, gen_degree)

def main():
    pass

def sort_tri_angle(tri):
    return tuple(sorted(tri))



if __name__ == '__main__':
    main()
