
import networkx as nx
from collections import Counter
from utils import network_topology
import numpy as np

def k_nearest_neighbors(graph):
    average_neighbor_degree = nx.average_neighbor_degree(graph)
    deg = nx.degree(graph)
    values = [{"points": []}]

    for i, (k, v) in enumerate(average_neighbor_degree.items()):
        values[0]["points"].append([deg[i], v * deg[i]])
    return values


def clustering(graph):
    h = graph.copy()
    cc = nx.clustering(h)
    degree = nx.degree(h)
    values = [{"points": []}]
    for k, v in cc.items():
        values[0]["points"].append([degree[k], v])
    return values

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

def get_parameter_real_world_network(graph):
    data = network_topology(graph)
    pos = np.array(list(nx.kamada_kawai_layout(graph).values()))
    for k, v in enumerate(pos):
        data["nodes"][k]["x"] = 500 * v[0]
        data["nodes"][k]["y"] = 500 * v[1]
    data["knn"] = k_nearest_neighbors(graph)
    data["degree"] = degree_his(graph)
    data["clustering"] = clustering(graph)
    return data


def real_world_network_test():

    dolphins = nx.read_gml("./data/real_networks/dolphins.gml", label="id")
    # 海豚网络 62 159
    karate = nx.read_gml("./data/real_networks/karate.gml", label="id")
    # 空手道俱乐部 34 78
    lesmis = nx.read_gml("./data/real_networks/lesmis.gml", label="id")
    # 悲惨世界 77  254

    data = {
        'dolphins': get_parameter_real_world_network(dolphins),
        'karate': get_parameter_real_world_network(karate),
        'lesmis': get_parameter_real_world_network(lesmis),
    }
    print(data["dolphins"])
    return data
