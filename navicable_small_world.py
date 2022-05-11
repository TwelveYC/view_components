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

def main():
    # g = nx.navigable_small_world_graph(10, r=2)
    # pos = {}
    # for i in g.nodes:
    #     pos[i] = [
    #         i[0] ,
    #         i[1] ,
    #     ]
    # nx.draw(g, pos=pos, node_size=10)
    # plt.show()

    # h = nx.to_undirected()
    v = []
    x = []
    for i in range(100):
        g = nx.navigable_small_world_graph(10, r=i/10)
        h = nx.to_undirected(g)
        sp = [len(i) for i in nx.shortest_path(h).values()]
        v.append(sum(sp) / len(sp))
        x.append(i)
    plt.plot(x, v)
    plt.show()


if __name__ == '__main__':
    main()