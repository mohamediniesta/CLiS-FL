from node import PowNode, MidNode, LowNode
from colorama import Fore

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


def display_client_information(selected_clients_list: list, selected_clients: list, number_weak_nodes: int,
                               number_mid_nodes: int, number_powerful_nodes: int, K: int):
    print("{0}Selected clients are : ".format(Fore.MAGENTA))
    print("{0}---------------------------------------------------------".format(Fore.MAGENTA))
    print(selected_clients_list)
    print("{0}---------------------------------------------------------".format(Fore.MAGENTA))
    print("[*] {0}{1} ({2}%) clients has been selected".format(Fore.MAGENTA, len(selected_clients), K * 100))
    print("[*] {0} There is {1} Weak nodes".format(Fore.RED, number_weak_nodes))
    print("[*] {0} There is {1} Medium power nodes".format(Fore.YELLOW, number_mid_nodes))
    print("[*] {0} There is {1} Powerful nodes".format(Fore.GREEN, number_powerful_nodes))
