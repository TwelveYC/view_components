"""
模型名称：ER 随即网络
代码：已有开源代码

实验：
100 个节点
1、增大过程中的网络图示
2、随着p 增大的相变过程


备注：

Ref：Gilbert E N. Random graphs[J]. The Annals of Mathematical Statistics, 1959, 30(4): 1141-1144.
"""

import networkx as nx
from matplotlib import pyplot as plt

def smooth(data):
    data_length = len(data)
    vs = []
    for k, v in enumerate(data):
        if k == 0 or k == data_length - 1:
            vs.append(v)
        else:
            vs.append((data[k - 1] + data[k + 1] + v) /  3)
    return vs


def main():
    N = 100
    v = []
    x = []
    for i in range(1, 101):
        g = nx.erdos_renyi_graph(N, i / 1000)
        if i % 20 == 0:
            print(i / 1000)
            # nx.draw(g, pos=nx.circular_layout(g))
            # plt.title("N=100, p={}".format(i / 1000))
            # plt.show()
        v.append(len(list(nx.connected_components(g))))
        x.append(i / 1000)

    plt.plot(x, smooth(v))
    plt.show()

def er_network_model_test():
    pass

if __name__ == '__main__':
    main()