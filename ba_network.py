
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

def main():
    g = nx.barabasi_albert_graph(100, 3, seed=7)
    deg = [i[1] for i in nx.degree(g)]
    fit = powerlaw.Fit(deg)
    fit.power_law.plot_pdf(linestyle="--", label="s {:.3f}".format(fit.power_law.alpha))
    plt.legend()
    plt.show()
if __name__ == '__main__':
    main()