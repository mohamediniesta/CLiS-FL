import uuid
import random
import numpy as np
from time import sleep
from colorama import Fore
from node import PowNode, MidNode, LowNode
from consumptionModel.StorageModel.StorageModel import StorageModel
from torchvision.datasets import MNIST, FashionMNIST, CIFAR100
from torchvision import transforms
from network.Network import Network
from utils.computation import chunk_list


def generate_node_id() -> str:
    node_id: str = uuid.uuid4().hex
    return node_id


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


def choose_dataset():
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
        train_dataset = MNIST(PATH, download=True, transform=apply_transform)
        test_dataset = MNIST(PATH, train=False, download=True, transform=apply_transform)

    if dataset_id == 2:
        train_dataset = FashionMNIST(PATH, download=True, transform=apply_transform)
        test_dataset = FashionMNIST(PATH, train=False, download=True, transform=apply_transform)

    if dataset_id == 3:
        train_dataset = CIFAR100(PATH, download=True, transform=apply_transform)
        test_dataset = CIFAR100(PATH, train=False, download=True, transform=apply_transform)

    print("{0}[+] You Have chose {1} dataset".format(Fore.LIGHTMAGENTA_EX, dataset.upper()))

    sleep(1.5)

    return dataset_id, train_dataset, test_dataset


def selected_to_dict(selected_clients: list) -> dict:
    clients = {}
    for client in selected_clients:
        clients[client.get_name()] = client.get_id()
    return clients


def sampling_data_to_clients(data, selected_client: list):
    num_clients = len(selected_client)
    num_items = int(len(data) / num_clients)
    dict_users, all_idxs = {}, [i for i in range(len(data))]
    for CLIENT in selected_client:
        storage_model = StorageModel(node=CLIENT)
        client_data = set(np.random.choice(all_idxs, num_items, replace=False))
        CLIENT.set_data(data=client_data, data_type="mnist")
        storage_model.add_to_storage(number_of_mega_bytes=5 * num_items)  # 5 Mega bytes per image (num_items)
        all_idxs = list(set(all_idxs) - CLIENT.get_data())


def split_nodes_networks(nodes):
    number_of_nodes = len(nodes)
    clients_chunk = chunk_list(lst=nodes, chunk_size=int(number_of_nodes / 5))
    i = 1
    networks = []
    for c in clients_chunk:
        network = Network(nodes=c, network_number=i, debug_mode=False)
        network.assign_ip_addresses()
        networks.append(network)
        i += 1
    return networks
