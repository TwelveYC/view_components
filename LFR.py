





import networkx as nx
from matplotlib import pyplot as plt
import powerlaw


def main():
    g = nx.LFR_benchmark_graph(250, 3, 1.5, 0.1, average_degree=5, min_community=10, max_iters=1000)
    nx.draw(g, pos=nx.kamada_kawai_layout(g))
    plt.show()

    # nx.write_gml(g, "vvv.gml")

def lfr_test():
    pass


if __name__ == '__main__':
    main()