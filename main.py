import networkx as nx
from collections import Counter
import powerlaw
from random import random
from networkx import utils
# 3 31
# 3.5 26

def main():
    g = nx.erdos_renyi_graph(50, 0.08)
    print(2 * g.number_of_edges() / g.number_of_nodes())
    print([i[1] for i in nx.degree(g)])


if __name__ == '__main__':
    main()
