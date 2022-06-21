import random
import numpy as np
from node import PowNode, MidNode, LowNode
from ConsumptionModel.StorageModel.StorageModel import StorageModel


def generateNodes(number_of_nodes: int) -> list:
    nodes = []
    for i in range(0, number_of_nodes):
        rate = random.randint(0, 2)
        if rate == 0:
            node = LowNode(name="Node {}".format(i), data="test")
        elif rate == 1:
            node = MidNode(name="Node {}".format(i), data="test")
        else:
            node = PowNode(name="Node {}".format(i), data="test")
        nodes.append(node)
    return nodes


def selected_to_dict(selected_clients: list) -> dict:
    clients = {}
    for client in selected_clients:
        clients[client.get_name()] = client.get_id()
    return clients


def sampling_data_to_clients(data, selected_client):
    num_clients = len(selected_client)
    num_items = int(len(data) / num_clients)
    dict_users, all_idxs = {}, [i for i in range(len(data))]
    for CLIENT in selected_client:
        storage_model = StorageModel(node=CLIENT)
        client_data = set(np.random.choice(all_idxs, num_items, replace=False))
        CLIENT.set_data(data=client_data, data_type="mnist")
        storage_model.add_to_storage(number_of_mega_bytes=5 * num_items)  # 5 Mega bytes per image (num_items)
        all_idxs = list(set(all_idxs) - CLIENT.get_data())
