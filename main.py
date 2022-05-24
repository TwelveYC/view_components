import json
from ba_network import ba_network_test
from er_network_model import er_network_model_test
from navigation_small_world import navigation_small_world_test
from config_model import config_model_test
from real_world_network import real_world_network_test
from small_world_network import small_world_network_test
from apollonian_network import appllonian_network_test
from bbv_model import bbv_model_test
from caveman import caveman_test
from flow_driven_model import flow_drive_model_test
from LFR import lfr_test
from weight_communities_network import weight_communities_test

exp_parameter = {
    "model_index": 7
}
Models = ["config", "scale-free", "real-world", "random-network", "small-world-network", "navigation-small-world", "bbv-model", "flow-drive", "weight-communities"]


def main():
    model_name = Models[exp_parameter["model_index"]]
    if model_name == "config":
        data = config_model_test()
    elif model_name == "scale-free":
        data = ba_network_test()
    elif model_name == "real-world":
        data = real_world_network_test()
    elif model_name == "random-network":
        data = er_network_model_test()
    elif model_name == "small-world-network":
        data = small_world_network_test()
    elif model_name == "navigation-small-world":
        data = navigation_small_world_test()
    elif model_name == "bbv-model":
        data = bbv_model_test()
    elif model_name == "flow-drive":
        data = flow_drive_model_test()
    elif model_name == "weight-communities":
        data = weight_communities_test()
    else:
        data = {}

    with open("./data/{}.json".format(model_name), "w") as fp:
        json.dump(data, fp)


if __name__ == '__main__':
    main()
