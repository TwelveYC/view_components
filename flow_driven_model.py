"""
流驱动模型

边的生成仅发生在新节点和老节点之间，而且边权的演化也是由新节点的加入而引起。

Ref: General dynamic of topology and traffic on weighted technological networks
"""
import networkx as nx
from itertools import product
from matplotlib import pyplot as plt
from numpy.random import choice
import numpy as np
from random import random
import powerlaw
from utils import network_topology


class FlowDrivenNetwork:
    def __init__(self, n0, W, m, w0):
        self.n0 = n0
        self.W = W
        self.m = m
        self.w0 = w0
        self.graph = nx.empty_graph(n0)
        self.nodes = list(self.graph.nodes)
        self.links = []

        ls = []
        for i in self.nodes:
            if i != n0 - 1:
                t = self.sort_edge(i, i + 1)
            else:
                t = self.sort_edge(0, i)
            ls.append([t[0], t[1], self.w0])
        self.graph.add_weighted_edges_from(ls, weight="w")
        self.links.extend(self.graph.edges)
        self.state = n0
        self.summarize_node_weight()



    def sort_edge(self, u, v):
        if u < v:
            return u, v
        else:
            return v, u

    def summarize_node_weight(self):
        attributes = nx.get_edge_attributes(self.graph, "w")
        node_weight = {}
        for i in self.graph.nodes:
            w = 0
            for j in nx.neighbors(self.graph, i):
                w += attributes.get(self.sort_edge(i, j), 0)
            node_weight[i] = w
        nx.set_node_attributes(self.graph, node_weight, "w")

    def step(self):
        node_attribute = nx.get_node_attributes(self.graph, "w")
        ps = []
        es = []
        for i in product(node_attribute.keys(), repeat=2):
            if i[0] != i[1] and i[0] < i[1]:
                es.append(i)
                ps.append(node_attribute[i[0]] * node_attribute[i[1]])
        ps = np.array(ps)
        ps = ps / np.sum(ps)
        wps = self.W * ps
        update_edges = []
        for k, v in enumerate(es):
            if random() <= wps[k]:
                update_edges.append(v)
        # nx.Graph().add_edges_from()
        ls = []
        for e in update_edges:
            if e in self.graph.edges:
                self.graph[e[0]][e[1]]["w"] += 1
            else:
                ls.append([e[0], e[1], self.w0])

        node_weight = []
        for i in self.graph.nodes:
            node_weight.append(node_attribute[i])
        node_weight = np.array(node_weight)
        node_weight = node_weight / np.sum(node_weight)
        ts = choice(self.graph.nodes, size=self.m, p=node_weight)

        for t in ts:
            v = self.sort_edge(self.state, t)
            ls.append([v[0], v[1], self.w0])

        self.graph.add_weighted_edges_from(ls, weight="w")
        self.summarize_node_weight()
        self.state += 1

def histogram(data, bins):
    density, bin_edges = np.histogram(data, bins=bins, density=True)
    data = []
    for i in range(bins):
        data.append({"y1": density[i], "x": bin_edges[i]})
    return data

def basic_simulation(W):
    N = 100
    n0 = 10
    net = FlowDrivenNetwork(n0, W, 3, 1)
    t = N - n0
    for i in range(t):
        net.step()
    data = network_topology(net.graph)
    node_attributes = nx.get_node_attributes(net.graph, "w")
    edge_attributes = nx.get_edge_attributes(net.graph, "w")

    pos = nx.kamada_kawai_layout(net.graph)
    for k, v in pos.items():
        data["nodes"][k]["x"], data["nodes"][k]["y"] = 500 * v[0], 500 * v[1]
        data["nodes"][k]["size"] = np.log10(node_attributes[k]) * 20

    for i, (k, v) in enumerate(edge_attributes.items()):
        data["links"][i]["size"] = edge_attributes[k]

    strength = list(nx.get_node_attributes(net.graph, "w").values())
    edge_weight = list(nx.get_edge_attributes(net.graph, "w").values())
    degree = [i[1] for i in nx.degree(net.graph)]
    data["pk"] = histogram(degree, 10)
    data["pw"] = histogram(edge_weight, 10)
    data["ps"] = histogram(strength, 10)

    strength_dict = nx.get_node_attributes(net.graph, "w")
    degree_dict = {i[0]:i[1] for i in nx.degree(net.graph)}

    temp = {"0": [], "1": [], "2": []}
    for i in nx.degree(net.graph):
        if i[1] in temp.keys():
            temp[i[1]].append(strength_dict[i[0]])
        else:
            temp[i[1]] = [strength_dict[i[0]]]
    skk = []
    for k, v in temp.items():
        if len(v) != 0:
           skk.append({"x": int(k), "y1": sum(v) / len(v)})
    skk = sorted(skk, key=lambda e: e["x"])
    wwkk = [{"points": []}]
    for i, j in net.graph.edges:
        wwkk[0]["points"].append([strength[i]*strength[j], degree_dict[i]*degree_dict[j]])
    data["skk"] = skk
    data["wwkk"] = wwkk
    return data


def main():
    pass


def flow_drive_model_test():
    ws = [1, 3, 5, 15]
    data = {}
    for d in ws:
        data[d] = basic_simulation(d)
    return data
