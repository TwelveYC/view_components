"""
模型名称：构型网络
代码：已有开源代码

实验：
50 个节点
1、生成为gamma=3 的无标度网络
2、生成为gamma=3.5 的无标度网络
3、生成为平均度为4 的er网络
4、生成为平均度为8 的er网络

备注：

Ref:Newman M E J. The structure and function of complex networks[J]. SIAM review, 2003, 45(2): 167-256.
"""
import networkx as nx
import powerlaw
from collections import Counter
import numpy as np
from matplotlib import pyplot as plt
from utils import smooth, network_topology
from random import sample


def degree_his(graph):
    h = graph.copy()
    deg = nx.degree(h)
    degree = [i[1] for i in deg]
    c = Counter(degree)
    values = []
    for k, v in c.items():
        values.append([k, v])
    values = sorted(values, key=lambda e: e[0])
    return values


def percolation(graph):
    h = graph.copy()
    es = h.edges
    ns = h.nodes
    degree = nx.degree(h)
    sort_degree = sorted(degree, key=lambda e: e[1], reverse=True)

    node_number = h.number_of_nodes()
    edge_number = h.number_of_edges()
    values = []
    for i in range(1, 101):
        hh = h.copy()
        remove_nodes = [j[0] for j in sort_degree[0: int((i * node_number) / 100)]]
        hh.remove_nodes_from(remove_nodes)
        if i != 100:
            size = len(max(list(nx.connected_components(hh)), key=len))
        else:
            size = 0
        values.append(size / node_number)

    return values


def clustering(graph):
    h = graph.copy()
    cc = nx.clustering(h)
    degree = nx.degree(h)
    values = []
    for k, v in cc.items():
        values.append([degree[k], v])
    return values


def get_config_network_model(t, s):
    # 3 101
    # 3.5 15
    # 3.2 184
    seq = nx.random_powerlaw_tree_sequence(100, gamma=t, tries=500000, seed=s)
    g = nx.configuration_model(seq)
    return g


def get_parameter(graph):
    data = network_topology(graph)
    data["degree"] = degree_his(graph)
    data["clustering"] = clustering(graph)
    data["percolation"] = percolation(graph)
    return data

def to_graph(graph):
    h = nx.Graph()
    es = []
    for i in graph.edges:
        if i[2] == 0:
            es.append([i[0], i[1]])
    h.add_edges_from(es)
    return h

def degree_summary(*args):
    values = []
    max_v = []
    for arg in args:
        max_v.extend(arg)
    max_v_v = max(max_v, key=lambda e:e[0])[0]
    for i in range(1, max_v_v + 1):
        values.append({"x": i})
    for k, arg in enumerate(args):
        for j in arg:
            values[j[0]-1]["y{}".format(k + 1)] = j[1]
    return values

def cluster_summary(*args):
    values = []
    for arg in args:
        values.append({"points": arg})
    return values

def percolation_summary(*args):
    values = []
    for i in range(1, 101):
        temp = {"x": i}
        for k, arg in enumerate(args):
            temp["y{}".format(k+1)] = arg[i - 1]
        values.append(temp)
    return values

def config_model_test():
    data = {}
    g3 = nx.read_gml("./data/nets/g3.gml")
    g35 = nx.read_gml("./data/nets/g35.gml")
    g32 = nx.read_gml("./data/nets/g32.gml")
    data3 = get_parameter(g3)
    data35 = get_parameter(g35)
    data32 = get_parameter(g32)
    pos3 = list(nx.kamada_kawai_layout(g3).values())
    pos35 = list(nx.kamada_kawai_layout(g35).values())
    pos32 = list(nx.kamada_kawai_layout(g32).values())


    for k, v in enumerate(pos3):
        data3["nodes"][k]["x"] = 500 * v[0]
        data3["nodes"][k]["y"] = 500 * v[1]

    for k, v in enumerate(pos35):
        data35["nodes"][k]["x"] = 500 * v[0]
        data35["nodes"][k]["y"] = 500 * v[1]

    for k, v in enumerate(pos32):
        data32["nodes"][k]["x"] = 500 * v[0]
        data32["nodes"][k]["y"] = 500 * v[1]

    data["g3"] = {"nodes": data3["nodes"], "links": data3["links"]}
    data["g35"] = {"nodes": data35["nodes"], "links": data35["links"]}
    data["g32"] = {"nodes": data32["nodes"], "links": data32["links"]}
    data["degree"] = degree_summary(data3["degree"], data35["degree"], data32["degree"])
    data["clustering"] = cluster_summary(data3["clustering"], data35["clustering"], data32["clustering"])
    data["percolation"] = percolation_summary(data3["percolation"], data35["percolation"], data32["percolation"])
    return data


if __name__ == '__main__':
    config_model_test()
