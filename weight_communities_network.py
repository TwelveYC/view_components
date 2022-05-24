"""
加权网络中的社区的存在


Emergence of communities in weighted networks

"""

import networkx as nx
from random import random, sample
import numpy as np
from numpy.random import choice
from matplotlib import pyplot as plt
import powerlaw


class WeightCommunityNetworks:
    def __init__(self, p_delta, delta):
        self.N = 1000
        self.pd = 0.01
        self.w0 = 1
        self.pr = 0.005
        self.p_delta = p_delta
        self.graph = nx.empty_graph(self.N)
        self.edges_weight = {}
        self.delta = delta
        nx.set_node_attributes(self.graph, {i: 0 for i in self.graph.nodes}, "w")
        self.nodes = list(range(self.N))
        self.links = []

    def step(self):
        self.global_attachment()
        self.local_attachment()
        self.node_deletion()
        t = self.graph.number_of_edges()
        return t

    def local_attachment(self):
        attributes = nx.get_edge_attributes(self.graph, "w")
        attributes_copy = attributes.copy()
        es_weight = []
        for i in self.graph.nodes:
            list_neighbors = list(nx.neighbors(self.graph, i))
            if len(list_neighbors) != 0:
                ps = []
                for p in list_neighbors:
                    t = self.sort_edge(i, p)
                    ps.append(attributes[t])
                ps = np.array(ps)
                ps = ps / np.sum(ps)
                j = choice(list_neighbors, p=ps)
                attributes_copy[self.sort_edge(i, j)] += self.delta
                j_neighbors = list(nx.neighbors(self.graph, j))
                j_neighbors.remove(i)
                if len(j_neighbors) != 0:
                    ps = []
                    for p in j_neighbors:
                        t = self.sort_edge(j, p)
                        # print(attributes)
                        # print(j_neighbors, j, p)
                        # print(list(self.graph.edges))
                        ps.append(attributes[t])
                    # print(ps)
                    ps = np.array(ps)
                    ps = ps / np.sum(ps)
                    k = choice(j_neighbors, p=ps)
                    tt = self.sort_edge(i, k)
                    if tt in self.links:
                        attributes_copy[tt] += self.delta
                    else:
                        if random() < self.p_delta:
                            attributes_copy[tt] = self.w0
                            es_weight.append([tt[0], tt[1]])
        self.graph.add_edges_from(es_weight)
        nx.set_edge_attributes(self.graph, attributes_copy, "w")
        self.summarize_node_weight()

    def global_attachment(self):
        es = []
        es_weight = []
        for i in self.graph.nodes:
            if random() <= self.pr:
                t = sample(self.nodes, 1)[0]
                if t != i:
                    e = self.sort_edge(i, t)
                    if e not in self.links:
                        es.append(e)
                        es_weight.append([e[0], e[1], self.w0])
        self.links.extend(es)
        self.graph.add_weighted_edges_from(es_weight, weight="w")
        self.summarize_node_weight()

    def summarize_node_weight(self):
        attributes = nx.get_edge_attributes(self.graph, "w")
        node_weight = {}
        for i in self.graph.nodes:
            w = 0
            for j in nx.neighbors(self.graph, i):
                w += attributes.get(self.sort_edge(i, j), 0)
            node_weight[i] = w
        nx.set_node_attributes(self.graph, node_weight, "w")

    def sort_edge(self, u, v):
        if u < v:
            return u, v
        else:
            return v, u

    def node_deletion(self):
        remove_links = []
        for i in self.nodes:
            if random() < self.pd:
                neighbors = list(nx.neighbors(self.graph, i))
                for i in neighbors:
                    ii = self.sort_edge(i, i)
                    if ii in self.links:
                        self.links.remove(ii)
                    remove_links.append(ii)
        self.graph.remove_edges_from(remove_links)
        self.summarize_node_weight()


def main():
    net = WeightCommunityNetworks(0.005, 0.1)
    # # 25 w
    v = []
    for i in range(3000):
        t = net.step()
        print(i, t)
        v.append(t)
    plt.plot(v)
    plt.show()


def weight_communities_test():
    pass

if __name__ == '__main__':
    main()
