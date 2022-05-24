"""
模型名称：导航模型
代码：已有开源代码

实验：
100 个节点
1、画网络模型
2、最优r 与网络直径的关系

问题 T 怎么算？

the average temporal shortest path length

备注：
Ref：Kleinberg J. The small-world phenomenon: An algorithmic perspective[C]//Proceedings of the thirty-second annual ACM symposium on Theory of computing. 2000: 163-170.
"""
import networkx as nx
from matplotlib import pyplot as plt
from random import sample
from utils import network_topology
import numpy as np
import pandas as pd
from itertools import product


def main():
    v = []
    x = []
    for i in range(100):
        g = nx.navigable_small_world_graph(10, r=i / 10)
        h = nx.to_undirected(g)
        sp = [len(i) for i in nx.shortest_path(h).values()]
        v.append(sum(sp) / len(sp))
        x.append(i)
    plt.plot(x, v)
    plt.show()


def average_shortest_path(g):
    return nx.average_shortest_path_length(g)


def single_navagable_shortest_path(g, source, target):
    navigation = True

    step = 0
    while navigation:
        step += 1
        neighbors = list(nx.neighbors(g, source))
        if target in neighbors:
            break
        manhattan_distances = []
        for i in neighbors:
            manhattan_distances.append([i, abs(i[0] - target[0]) + abs(i[1] - target[1])])
        source = min(manhattan_distances, key=lambda e: e[1])[0]

    return step


def single_direction_navaigable_shortest_path(g, source, target, router):
    navigation = True

    step = 0
    while navigation:
        step += 1
        neighbors = router[source]
        if target in neighbors:
            break
        manhattan_distances = []
        for i in neighbors:
            manhattan_distances.append([i, abs(i[0] - target[0]) + abs(i[1] - target[1])])
        source = min(manhattan_distances, key=lambda e: e[1])[0]

    return step


def navagable_shortest_path(g):
    ns = list(g.nodes)
    router = {}
    is_directed = g.is_directed()
    if is_directed:
        for i in g.out_edges:
            if i[0] not in router.keys():
                router[i[0]] = [i[1]]
            else:
                router[i[0]].append(i[1])

    distances = []
    for i in ns:
        for j in ns:
            if i != j:
                source, target = i, j
                if is_directed:
                    distances.append(single_direction_navaigable_shortest_path(g, source, target, router))
                else:
                    distances.append(single_navagable_shortest_path(g, source, target))
    return sum(distances) / len(distances)


def get_pos(graph):
    data = network_topology(graph)
    for k, v in enumerate(graph.nodes):
        data["nodes"][k]["x"], data["nodes"][k]["y"] = v[0] * 10, v[1] * 10
    return data


def get_beta(x):
    if 0 <= x < 2:
        return (2 - x) / 3
    else:
        return (x - 2) / (x - 1)


def navigation_small_world_test():
    # g1 = nx.navigable_small_world_graph(1000, r=1).to_undirected()
    # g2 = nx.navigable_small_world_graph(1000, r=2).to_undirected()
    # g5 = nx.navigable_small_world_graph(1000, r=5).to_undirected()
    # print("done")
    # ns = g1.nodes
    # ods = sample(product(ns, repeat=2), 1000)
    # print(ods)

    g1 = nx.navigable_small_world_graph(10, r=1).to_undirected()
    g5 = nx.navigable_small_world_graph(10, r=5).to_undirected()
    g2 = nx.navigable_small_world_graph(10, r=2).to_undirected()
    data = {
        "g1": get_pos(g1),
        "g5": get_pos(g5),
        "g2": get_pos(g2)
    }
    beta_alpha = []
    for i in range(1, 31):
        x = i / 10
        beta_alpha.append({
            "x": x,
            "y1": get_beta(x)
        })
    data["beta"] = beta_alpha
    df = pd.read_csv("data/导航网络xyz.csv")
    distance = []
    for k, v in enumerate(df["x"]):
        distance.append({
            "x": v,
            "y1": df["y"][k]
        })
    data["distance"] = distance
    navagable_N_distance = []
    for i in range(5, 20):
        g = nx.navigable_small_world_graph(i).to_undirected()
        navagable_N_distance.append({
            "x": i,
            "y1": navagable_shortest_path(g)
        })
    data["distance_N"] = navagable_N_distance

    # pos = {}
    # for i in g1:
    #     pos[i] = i
    # nx.draw(g1, pos=pos, with_labels=True)
    # plt.show()
    #
    #
    # nx.draw(g2, pos=pos)
    # plt.show()
    #
    #
    # nx.draw(g5, pos=pos)
    # plt.show()
    # print(navagable_shortest_path(g1))
    # print(navagable_shortest_path(g5))
    # print(navagable_shortest_path(g2))
    # 10.686249699879951
    # 30.27379991996799
    # 13.227296518607442

    # single_navagable_shortest_path(g1, (0, 0), (9, 9))
    #
    # distance = []
    # for i in range(1, 71, 1):
    #     v = i / 10
    #     g = nx.navigable_small_world_graph(10, r=v).to_undirected()
    #     distance.append({
    #         "x": v,
    #         "y1": average_shortest_path(g),
    #         "y2": navagable_shortest_path(g)
    #     })
    # df = pd.DataFrame(distance)
    # print(df)
    # plt.plot(df["x"], df["y1"], label="y1")
    # plt.plot(df["x"], df["y2"], label="y2")
    # plt.legend()
    # plt.show()
    # data["distance"] = distance
    # navagable_N_distance = []
    # for i in range(5, 20):
    #     g = nx.navigable_small_world_graph(i).to_undirected()
    #     navagable_N_distance.append({
    #         "x": i,
    #         "y1": navagable_shortest_path(g)
    #     })
    # data["distance_N"] = navagable_N_distance
    # beta_alpha = []
    # for i in range(1, 71, 1):
    #     v = i / 10
    #     print(i)
    #     beta_alpha.append({
    #         "x": v,
    #         "y1": get_beta(v)
    #     })
    #
    # data["beta"] = beta_alpha
    # data = {"x": [], "y": []}
    # for i in range(20, 71, 10):
    #     data["x"].append(i)
    #     g = nx.navigable_small_world_graph(i, r=2).to_undirected()
    #     data["y"].append(navagable_shortest_path(g))
    # df = pd.DataFrame(data)
    # df.to_csv("a.csv")
    # plt.plot(df["x"], df["y"])
    # plt.show()

    return data


def least_squares(x, y):
    ones = np.ones((len(x)))
    A = np.c_[ones, x]
    ATA = A.T.dot(A)
    ATb = A.T.dot(y)
    inv_ATA = np.linalg.inv(ATA)
    solution = inv_ATA.dot(ATb)
    return solution

