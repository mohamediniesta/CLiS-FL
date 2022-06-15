from colorama import init, Fore
from utils.generation import generateNodes
from ClientSelection import RandomClientSelection
from node import PowNode, MidNode, LowNode

init(autoreset=True)

if __name__ == '__main__':

    number_of_nodes = int(input("{0}How Many nodes do you want to simulate ?\n".format(Fore.YELLOW)))
    clients = generateNodes(number_of_nodes=number_of_nodes)
    K = int(input("{0}What percentage of participating clients do you want?\n".format(Fore.YELLOW)))
    K = K / 100
    selected_clients = RandomClientSelection(nodes=clients, K=K, debug_mode=False).randomClientSelection()
    number_weak_nodes = 0
    number_mid_nodes = 0
    number_powerful_nodes = 0
    clients = {}
    for client in selected_clients:
        clients[client.get_name()] = client.get_id()
        if isinstance(client, LowNode):
            number_weak_nodes = number_weak_nodes + 1
        if isinstance(client, MidNode):
            number_mid_nodes = number_mid_nodes + 1
        if isinstance(client, PowNode):
            number_powerful_nodes = number_powerful_nodes + 1

    print("{0}Selected clients are : ".format(Fore.MAGENTA))
    print("{0}---------------------------------------------------------".format(Fore.MAGENTA))
    print(clients)
    print("{0}---------------------------------------------------------".format(Fore.MAGENTA))
    print("[*] {0}{1} ({2}%) clients has been selected".format(Fore.MAGENTA, len(selected_clients), K * 100))
    print("[*] {0} There is {1} Weak nodes".format(Fore.RED, number_weak_nodes))
    print("[*] {0} There is {1} Medium power nodes".format(Fore.YELLOW, number_mid_nodes))
    print("[*] {0} There is {1} Powerful nodes".format(Fore.GREEN, number_powerful_nodes))
