
"""
模型名称：构型网络
代码：已有开源代码

实验：
50 个节点
1、生成N = 100，m=3的无标度网络
2、计算其幂律为 3

备注：

Ref: Barabási A L, Albert R. Emergence of scaling in random networks[J]. science, 1999, 286(5439): 509-512.
"""
import networkx as nx
import powerlaw
from matplotlib import pyplot as plt
from collections import Counter
from random import sample
from utils import network_topology, smooth
import pandas as pd
import numpy as np


def degree_his(graph):
    h = graph.copy()
    deg = nx.degree(h)
    degree = [i[1] for i in deg]
    c = Counter(degree)
    values = []
    for k, v in c.items():
        values.append({"x": k, "y1": v})
    values = sorted(values, key=lambda e:e["x"])
    return values


def percolation(graph):
    h = graph.copy()
    es = h.edges
    ns = h.nodes
    degree = nx.degree(h)
    sort_degree = sorted(degree, key=lambda e:e[1], reverse=True)

    node_number = h.number_of_nodes()
    edge_number = h.number_of_edges()
    values = []
    values_1 = []
    values_2 = []
    for i in range(1, 101):
        remove_nodes = sample(ns, int((i * node_number) / 100))
        hh = h.copy()
        hh.remove_nodes_from(remove_nodes)
        if i != 100:
            size = len(max(list(nx.connected_components(hh)), key=len))
        else:
            size = 0
        values_1.append(size / node_number)


    for i in range(1, 101):
        hh = h.copy()
        remove_nodes = [j[0] for j in sort_degree[0: int((i * node_number) / 100)]]
        hh.remove_nodes_from(remove_nodes)
        if i != 100:
            size = len(max(list(nx.connected_components(hh)), key=len))
        else:
            size = 0
        values_2.append(size / node_number)
    values_1 = smooth(smooth(values_1))
    values_2 = smooth(smooth(values_2))
    for i in range(1, 101):
        values.append({
            "x": i,
            "y1": values_1[i - 1],
            "y2": values_2[i - 1]
        })

    return values



def clustering(graph):
    h = graph.copy()
    cc = nx.clustering(h)
    degree = nx.degree(h)
    values = [{"points": []}]
    for k, v in cc.items():
        values[0]["points"].append([degree[k], v])
    return values

from math import log10
def ba_network_test():
    g = nx.read_gml("data/nets/scale_free_networks.gml")
    data = network_topology(g)
    pos = np.array(list(nx.kamada_kawai_layout(g).values()))
    deg = {i[0]:i[1] for i in nx.degree(g)}
    for k, v in enumerate(pos):
        data["nodes"][k]["x"] = 500 * v[0]
        data["nodes"][k]["y"] = 500 * v[1]
        data["nodes"][k]["size"] = 60 * log10(deg[str(k)])
        data["nodes"][k]["fColor"] = "#fefeff"
    data["clustering"] = clustering(g)
    data["degree"] = degree_his(g)
    data["percolation"] = percolation(g)
    return data

