import networkx as nx
import json
import numpy as np
import powerlaw
from itertools import product
from matplotlib import pyplot as plt


# 180
# 404
# 7.36
# ba
seq_3 = [16, 6, 3, 6, 23, 21, 8, 18, 15, 9, 12, 10, 5, 9, 11, 13, 8, 6, 5, 14, 5, 7, 6, 4, 5, 8, 7, 5, 5, 4, 5, 6, 5, 6, 4, 4, 5, 5, 4, 5, 4, 7, 5, 4, 4, 4, 4, 5, 4, 4]
# er
seq = [4, 10, 6, 5, 9, 7, 9, 10, 2, 9, 5, 7, 5, 6, 8, 10, 8, 5, 6, 10, 6, 9, 4, 5, 8, 2, 6, 8, 6, 3, 5, 5, 6, 9, 5, 9, 7, 6, 7, 4, 7, 14, 9, 6, 7, 6, 5, 9, 4, 8]


def main():
    g = nx.barabasi_albert_graph(100, 3)
    deg = []
    for i in nx.degree(g):
        deg.append(i[1])
    print(g.degree)
    nx.LFR_benchmark_graph




if __name__ == '__main__':
    main()




