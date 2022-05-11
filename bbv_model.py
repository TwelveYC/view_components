"""
bbv 加权动态演化网络
1、bbv 模型生成
2、度和强度的分布满足幂律


Weighted evolving networks: coupling topology and weight dynamics
"""

import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from numpy.random import choice
import powerlaw


class BBVModel:
    def __init__(self, n0, m, delta, w0):
        self.n0 = n0
        self.m = m
        self.delta = delta
        self.w0 = w0
        self.graph = nx.empty_graph(n0)
        self.nodes = list(self.graph.nodes)

        ls = []
        for i in self.nodes:
            if i != n0 - 1:
                t = self.sort_edge(i, i + 1)
            else:
                t = self.sort_edge(0, i)
            ls.append(t)
        self.graph.add_edges_from(ls)
        self.state = n0
        node_weight = {}
        for i in self.nodes:
            node_weight[i] = {"w": 2}
        nx.set_node_attributes(self.graph, node_weight)

    def step(self):
        es = []
        node_attributes = nx.get_node_attributes(self.graph, "w")
        node_attributes_copy = node_attributes.copy()
        node_weight = np.array(list(node_attributes.values()))
        node_weight = node_weight / np.sum(node_weight)
        ts = choice(self.nodes, size=self.m, p=node_weight)
        node_attributes_copy[self.state] = self.m * self.w0
        for t in ts:
            node_attributes_copy[t] += (self.w0 + self.delta)
            es.append(self.sort_edge(self.state, t))
        self.graph.add_edges_from(es)
        for k, v in node_attributes_copy.items():
            self.graph.nodes[k]["w"] = v

        self.nodes.append(self.state)
        self.state += 1

    def sort_edge(self, u, v):
        if u < v:
            return u, v
        else:
            return v, u

def basic_simulation(delta):
    N = 700
    n0 = 10
    net = BBVModel(10, 2, delta, 1)
    for i in range(N - n0):
        print(i, N - n0)
        net.step()

    # deg = [i[1] for i in nx.degree(net.graph)]
    # fit = powerlaw.Fit(deg)
    # fit.power_law.plot_pdf(linestyle="--", label="k {:.3f} delta {}".format(fit.power_law.alpha, delta))

    s = list(nx.get_node_attributes(net.graph, "w").values())
    fit = powerlaw.Fit(s)
    fit.power_law.plot_pdf(linestyle="--", label="s {:.3f} delta {}".format(fit.power_law.alpha, delta))


def main():
    ds = [0.5, 1, 2, 5]
    for d in ds:
        basic_simulation(d)
    plt.legend()
    plt.show()






if __name__ == '__main__':
    main()
