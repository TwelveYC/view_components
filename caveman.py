"""
caveman 网络
很高的聚类系数(1 - (6 / (k^2 - 1)))
corresponding characteristic path
L = n / 2(k+ 1)



Hence, the connected caveman graph can be used as a benchmark for a “large, highly clustered graph.
Watts D J. Networks, dynamics, and the small-world phenomenon[J]. American Journal of sociology, 1999, 105(2): 493-527.
"""
import networkx as nx
from matplotlib import pyplot as plt
def main():
    g = nx.connected_caveman_graph(9, 4)
    nx.draw(g, pos=nx.kamada_kawai_layout(g))
    print(nx.average_clustering(g))
    plt.show()

    sp = [len(i) for i in nx.shortest_path(g).values()]
    print(sp)
    print(sum(sp) / len(sp))
    print(g.number_of_nodes() / (2 * (4 + 1)))



if __name__ == '__main__':
    main()