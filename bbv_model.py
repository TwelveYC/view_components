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
from utils import network_topology


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
        edge_weight = {}
        for i in self.graph.edges:
            edge_weight[i] = {"w": self.w0}
        nx.set_edge_attributes(self.graph, edge_weight)

    def step(self):
        es = []
        node_attributes = nx.get_node_attributes(self.graph, "w")
        node_attributes_copy = node_attributes.copy()
        edge_attributes = nx.get_edge_attributes(self.graph, "w")
        edge_attributes_copy = edge_attributes.copy()
        node_weight = np.array(list(node_attributes.values()))
        node_weight = node_weight / np.sum(node_weight)
        ts = choice(self.nodes, size=self.m, p=node_weight)
        node_attributes_copy[self.state] = self.m * self.w0
        for t in ts:
            node_attributes_copy[t] += (self.w0 + self.delta)
            sort_edge = self.sort_edge(self.state, t)
            es.append(sort_edge)
            edge_attributes_copy[sort_edge] = self.w0
        self.graph.add_edges_from(es)
        for t in ts:
            ps = []
            neighbors = list(nx.neighbors(self.graph, t))
            for i in neighbors:
                ps.append(edge_attributes_copy[self.sort_edge(t, i)])
            ps_sum = sum(ps)
            for i in neighbors:
                sort_edge = self.sort_edge(t, i)
                edge_attributes_copy[sort_edge] += self.delta * edge_attributes_copy[sort_edge] / ps_sum

        for k, v in node_attributes_copy.items():
            self.graph.nodes[k]["w"] = v
        nx.set_edge_attributes(self.graph, edge_attributes_copy, "w")

        self.nodes.append(self.state)
        self.state += 1

    def sort_edge(self, u, v):
        if u < v:
            return u, v
        else:
            return v, u


def static_sort_edge(u, v):
    if u < v:
        return u, v
    else:
        return v, u


def basic_simulation(delta):
    N = 100
    n0 = 10
    net = BBVModel(10, 2, delta, 1)
    for i in range(N - n0):
        net.step()
    data = network_topology(net.graph)
    node_attributes = nx.get_node_attributes(net.graph, "w")
    edge_attributes = nx.get_edge_attributes(net.graph, "w")
    # for k, v in enumerate(net.graph.nodes):
    #     data["nodes"][k]["x"]

    pos = nx.kamada_kawai_layout(net.graph)
    for k, v in pos.items():
        data["nodes"][k]["x"], data["nodes"][k]["y"] = 500 * v[0], 500 * v[1]
        data["nodes"][k]["size"] = np.log10(node_attributes[k]) * 40
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


    # print(len(nx.get_edge_attributes(net.graph, "w")))
    # print(net.graph.number_of_edges())
    # deg = [i[1] for i in nx.degree(net.graph)]
    # fit = powerlaw.Fit(deg)
    # fit.power_law.plot_pdf(linestyle="--", label="k {:.3f} delta {}".format(fit.power_law.alpha, delta))
    # s = list(nx.get_node_attributes(net.graph, "w").values())
    # print(net.graph.number_of_edges())
    # print(net.graph.number_of_nodes())
    # fit = powerlaw.Fit(s)
    # fit.power_law.plot_pdf(linestyle="--", label="s {:.3f} delta {}".format(fit.power_law.alpha, delta))

def histogram(data, bins):
    density, bin_edges = np.histogram(data, bins=bins, density=True)
    data = []
    for i in range(bins):
        data.append({"y1": density[i], "x": bin_edges[i]})
    return data


def bbv_model_test():
    ds = [0.5, 1, 2, 5]
    data = {}
    for d in ds:
        data[d] = basic_simulation(d)
    return data




