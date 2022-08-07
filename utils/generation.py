import uuid
import random
import numpy as np
from time import sleep
from colorama import Fore
from torchvision import transforms
from network.Network import Network
from utils.computation import chunk_list
from node import PowNode, MidNode, LowNode
from torchvision.datasets import MNIST, FashionMNIST, CIFAR100
from consumptionModel.StorageModel.StorageModel import StorageModel


def generateNode_id() -> str:
    node_id: str = uuid.uuid4().hex
    return node_id


def generateNodes(number_of_nodes: int, data) -> list:
    print("{0}[*] Generating {1} node(s) with random data".format(Fore.LIGHTMAGENTA_EX, number_of_nodes))
    nodes = []
    min_length = int(len(data) / number_of_nodes)
    dataID_list = [i for i in range(len(data))]
    for i in range(0, number_of_nodes):
        rate = random.randint(0, 2)
        node = LowNode(name="Node {}".format(i), data="test") if rate == 0 else \
            MidNode(name="Node {}".format(i), data="test") if rate == 1 else \
                PowNode(name="Node {}".format(i), data="test")
        # ? Set the data.
        num_items = random.randint(min_length, len(data) / 10)
        client_data = set(np.random.choice(dataID_list, num_items, replace=False))
        node.set_data(data=client_data, data_type="mnist")

        StorageModel(node=node). \
            add_to_storage(number_of_mega_bytes=2 * num_items)  # ? 2 Mega bytes per image (num_items)

        nodes.append(node)

    return nodes


def chooseDataset():
    dataset_list = {1: "mnist", 2: "fashion_mnist", 3: "cifar"}
    dataset_id = int(input('''{0}Which dataset do you want to use ?{1}
    1 - Mnist
    2 - Fashion Mnist
    3 - Cifar\n{0}> '''.format(Fore.LIGHTYELLOW_EX, Fore.YELLOW)))
    while dataset_id != 1 and dataset_id != 2 and dataset_id != 3:
        print("{0}[-] Error !, Please select id from 1 to 3".format(Fore.LIGHTRED_EX))
        dataset_id = int(input('''{0}Which dataset do you want to use ?{1}
        1 - Mnist
        2 - Fashion Mnist
        3 - Cifar\n{0}> '''.format(Fore.LIGHTYELLOW_EX, Fore.YELLOW)))

    dataset = dataset_list[dataset_id]
    apply_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    PATH = "datasets/{0}/".format(dataset)

    if dataset_id == 1:
        train_dataset, test_dataset = MNIST(PATH, download=True, transform=apply_transform), \
                                      MNIST(PATH, train=False, download=True, transform=apply_transform)
    elif dataset_id == 2:
        train_dataset, test_dataset = FashionMNIST(PATH, download=True, transform=apply_transform), \
                                      FashionMNIST(PATH, train=False, download=True, transform=apply_transform)
    else:
        train_dataset, test_dataset = CIFAR100(PATH, download=True, transform=apply_transform), \
                                      CIFAR100(PATH, train=False, download=True, transform=apply_transform)

    print("{0}[+] You Have chose {1} dataset".format(Fore.LIGHTMAGENTA_EX, dataset.upper()))

    sleep(1.5)

    return dataset_id, train_dataset, test_dataset


def selectedToDict(selected_clients: list) -> dict:
    clients = {}
    for client in selected_clients:
        clients[client.getName()] = client.getId()
    return clients


def splitNodesNetworks(nodes):
    number_of_nodes = len(nodes)
    clients_chunk = chunk_list(lst=nodes, chunk_size=int(number_of_nodes / 5))
    i = 1
    networks = []
    for c in clients_chunk:
        network = Network(nodes=c, network_number=i, debug_mode=False)
        network.assignIpAddresses()
        networks.append(network)
        i += 1
    return networks
