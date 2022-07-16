from node import PowNode, MidNode, LowNode
import matplotlib.pyplot as plt
from colorama import Fore
import numpy as np


def show_results(train_loss, clients_acc):
    print("-" * 30)
    print(f'Global Training Loss : {np.mean(np.array(train_loss))}')
    print("Local accuracy of each client : ")
    print("-" * 30)
    print(clients_acc)
    print("-" * 30)


def draw_graph(accuracy_data: dict = None, energy_data: dict = None, down_data: dict = None):
    methods = list(accuracy_data.keys())
    values = list(accuracy_data.values())

    fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, sharex=True,
                                        figsize=(16, 8))

    fig.canvas.set_window_title('Federated Learning simulation')

    # ? creating the bar plot
    ax0.bar(methods, values, color='maroon', width=0.4)
    ax0.set_title("Global Accuracy")
    ax0.set_xlabel("Methods")
    ax0.set_ylabel("Accuracy (%)")

    methods = list(energy_data.keys())
    values = list(energy_data.values())

    ax1.bar(methods, values, color='gold', width=0.4)
    ax1.set_title("Energy Consumption")
    ax1.set_ylabel("Energy ( mAh)")
    ax1.set_xlabel("Methods")

    methods = list(down_data.keys())
    values = list(down_data.values())

    ax2.bar(methods, values, color='purple', width=0.4)
    ax2.set_title("Rejected Clients")
    ax2.set_ylabel("Number of rejected clients")
    ax2.set_xlabel("Methods")

    plt.show()


def count_rejected_clients(clients: list) -> int:
    n = 0
    for client in clients:
        if client.get_status() == 0:
            n = n + 1
    return n


def count_clients(selected_clients: list) -> (int, int, int):
    number_weak_nodes = 0
    number_mid_nodes = 0
    number_powerful_nodes = 0

    for client in selected_clients:
        if isinstance(client, LowNode):
            number_weak_nodes = number_weak_nodes + 1
        if isinstance(client, MidNode):
            number_mid_nodes = number_mid_nodes + 1
        if isinstance(client, PowNode):
            number_powerful_nodes = number_powerful_nodes + 1

    return number_weak_nodes, number_mid_nodes, number_powerful_nodes


def display_client_information(selected_clients_list: dict, selected_clients: list, number_weak_nodes: int,
                               number_mid_nodes: int, number_powerful_nodes: int, K: float):
    print("{0}Selected clients are : ".format(Fore.MAGENTA))
    print("{0}---------------------------------------------------------".format(Fore.MAGENTA))
    print(selected_clients_list)
    print("{0}---------------------------------------------------------".format(Fore.MAGENTA))
    print("[*] {0}{1} ({2}%) clients has been selected".format(Fore.MAGENTA, len(selected_clients), K * 100))
    print("[*] {0} There is {1} Weak nodes".format(Fore.RED, number_weak_nodes))
    print("[*] {0} There is {1} Medium power nodes".format(Fore.YELLOW, number_mid_nodes))
    print("[*] {0} There is {1} Powerful nodes".format(Fore.GREEN, number_powerful_nodes))
