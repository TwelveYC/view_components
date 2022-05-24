def network_topology(graph):
    h = graph.copy()
    data = {"nodes": [], "links": []}
    for i in h.nodes:
        data["nodes"].append({"id": i})
    for i in h.edges:
        data["links"].append({"source": i[0], "target": i[1]})
    return data


def smooth(data):
    data_length = len(data)
    res = []
    for i in range(data_length):
        if i != 0 and i != data_length - 1:
            res.append((data[i - 1] + data[i] + data[i + 1]) / 3)
        else:
            res.append(data[i])
    return res

