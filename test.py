import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from random import random
import networkx as nx
plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题




def main():
    v = []
    for i in range(7):
        v.append({"x": i, "y1": random()})
    for i in range(7):
        v.append({"x": i, "y2": random()})
    print(v)

    # df = pd.read_csv("a.csv")
    # plt.plot(np.log10(df["x"]), df["y"], label="单对数")
    # plt.title("单对数")
    # plt.show()
    # plt.plot(np.log10(df["x"]), np.log10(df["y"]), label="双对数")
    # plt.title("双对数")
    # plt.show()
#    实现 （周三）
#    生成数据（）
#




if __name__ == '__main__':
    main()
