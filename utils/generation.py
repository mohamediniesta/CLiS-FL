# pylint: disable = C0114, C0115, C0116, C0103

import random
from time import sleep
import numpy as np
from colorama import Fore
from torchvision import transforms
from torchvision.datasets import MNIST, FashionMNIST, CIFAR100
from network.Network import Network
from utils.computation import chunk_list
from node import PowNode, MidNode, LowNode
from consumptionModel.StorageModel.StorageModel import StorageModel
from constants.resource_constants import IMAGE_SIZE, LOW_NODE_DISTRIBUTION, POW_NODE_DISTRIBUTION, MED_NODE_DISTRIBUTION, CALCULATE_RESOURCES


def generate_nodes(number_of_nodes: int, data) -> list:
    print(f"{Fore.LIGHTMAGENTA_EX}[*] Generating {number_of_nodes} node(s) with random data")
    nodes = []
    min_length = int(len(data) / number_of_nodes)
    data_id_list = list(range(len(data)))
    random_node_list = [0, 1, 2]  # ? 0 = Low , 1 = Medium , 2 = Pow
    data_percentage = 0.05  # ? 5%
    for i in range(0, number_of_nodes):
        rate = random.choices(random_node_list,
                              [LOW_NODE_DISTRIBUTION, MED_NODE_DISTRIBUTION,
                               POW_NODE_DISTRIBUTION])[0]
        # ? Randomly pick a category of node.
        node = LowNode(name=f"Node {i}") if rate == 0 else \
            MidNode(name=f"Node {i}") if rate == 1 else \
                PowNode(name=f"Node {i}")
        # ? Set the data. ( Using CPU usage, etc .. ), randomly set the data size.
        num_items = random.randint(min_length, len(data) * data_percentage)
        client_data = set(np.random.choice(data_id_list, num_items, replace=False))
        # ? Put the random data on nodes.
        node.set_data(data=client_data, data_type="mnist")
        if CALCULATE_RESOURCES:
            StorageModel(node=node). \
                add_to_storage(
                number_of_mega_bytes=IMAGE_SIZE * num_items)  # ? 800 Kilo bytes per image (num_items)

        nodes.append(node)

    return nodes


def choose_dataset():
    dataset_list = {1: "mnist", 2: "fashion_mnist", 3: "cifar"}
    dataset_id = int(input(f'''{Fore.LIGHTYELLOW_EX}Which dataset do you want to use ?{Fore.YELLOW}
    1 - Mnist
    2 - Fashion Mnist
    3 - Cifar\n{Fore.LIGHTYELLOW_EX}> '''))
    while dataset_id not in (1, 2, 3):
        print(f"{Fore.LIGHTRED_EX}[-] Error !, Please select id from 1 to 3")
        dataset_id = int(input(f'''{Fore.LIGHTYELLOW_EX}Which dataset do you want to use ?
        {Fore.YELLOW}
        1 - Mnist
        2 - Fashion Mnist
        3 - Cifar\n{Fore.LIGHTYELLOW_EX}> '''))

    dataset = dataset_list[dataset_id]
    apply_transform = transforms.Compose([transforms.ToTensor(),
                                          transforms.Normalize((0.1307,), (0.3081,))])

    PATH = f"datasets/{dataset}/"

    if dataset_id == 1:
        train_dataset, test_dataset = MNIST(PATH, download=True, transform=apply_transform), \
                                      MNIST(PATH, train=False, download=True,
                                            transform=apply_transform)
    elif dataset_id == 2:
        train_dataset, test_dataset = FashionMNIST(PATH, download=True,
                                                   transform=apply_transform), \
                                      FashionMNIST(PATH, train=False, download=True,
                                                   transform=apply_transform)
    else:
        train_dataset, test_dataset = CIFAR100(PATH, download=True, transform=apply_transform), \
                                      CIFAR100(PATH, train=False, download=True,
                                               transform=apply_transform)

    print(f"{Fore.LIGHTMAGENTA_EX}[+] You Have chose {dataset.upper()} dataset")

    sleep(1.5)

    return dataset_id, train_dataset, test_dataset


def selected_to_dict(selected_clients: list) -> dict:
    return {client.get_name(): client.get_id() for client in selected_clients}


def split_nodes_networks(nodes):
    number_of_nodes = len(nodes)
    clients_chunk = chunk_list(lst=nodes, chunk_size=int(number_of_nodes / 5))
    networks = []

    for i, c in enumerate(clients_chunk, start=1):
        network = Network(nodes=c, network_number=i, debug_mode=False)
        network.assign_ip_addresses()
        networks.append(network)

    return networks
