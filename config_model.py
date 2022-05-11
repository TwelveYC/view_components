
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
import numpy as np
from matplotlib import pyplot as plt

config_parameter = {
    "exp_mode": "possion"
}


def main():
    if config_parameter["exp_mode"] == "power_law":
        exp_1()
        exp_2()
    elif config_parameter["exp_mode"] == "possion":
        exp_3()
        exp_4()
    plt.legend()
    plt.show()

def exp_1():
    t = 3
    s = 31
    seq = nx.random_powerlaw_tree_sequence(50, gamma=t, tries=50000, seed=s)
    g = nx.configuration_model(seq)
    deg = [i[1] for i in nx.degree(g)]
    # deg = np.array(deg) + 1
    fit = powerlaw.Fit(deg)
    fit.power_law.plot_pdf(color="g", linestyle="--", label="{:.3f}".format(fit.power_law.alpha))
    v = fit.power_law.alpha

def exp_2():
    t = 3.5
    s = 367
    sequence = nx.random_powerlaw_tree_sequence(50, gamma=t, tries=50000, seed=s)
    g = nx.configuration_model(sequence)
    deg = [i[1] for i in nx.degree(g)]
    deg = np.array(deg) + 1
    fit = powerlaw.Fit(deg)
    fit.power_law.plot_pdf(color="b", linestyle="--", label="{:.3f}".format(fit.power_law.alpha))
    v = fit.power_law.alpha
    print(v)

def exp_3():
    seq = [3, 8, 3, 3, 3, 5, 5, 2, 5, 4, 3, 8, 2, 1, 5, 4, 3, 4, 5, 4, 5, 1, 4, 7, 5, 5, 7, 10, 4, 1, 2, 4, 1, 2, 3, 4, 4, 2, 10, 6, 2, 2, 3, 2, 6, 2, 1, 4, 6, 7]
    g = nx.configuration_model(seq)
    deg = [i[1] for i in nx.degree(g)]
    plt.hist(deg, bins=50, label="4")

def exp_4():
    seq = [8, 6, 15, 9, 7, 6, 9, 13, 7, 8, 6, 7, 7, 7, 8, 5, 10, 8, 10, 11, 10, 10, 7, 9, 9, 13, 9, 8, 7, 11, 8, 8, 7, 6, 7, 7, 8, 11, 4, 9, 10, 5, 8, 5, 7, 4, 10, 6, 10, 6]
    g = nx.configuration_model(seq)
    deg = [i[1] for i in nx.degree(g)]
    plt.hist(deg, bins=50, label="8")

if __name__ == '__main__':
    main()