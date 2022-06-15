from colorama import init, Fore
from utils.generation import generateNodes, selected_to_dict
from utils.stats import count_clients
from ClientSelection import RandomClientSelection

init(autoreset=True)

if __name__ == '__main__':

    number_of_nodes = int(input("{0}How Many nodes do you want to simulate ?\n".format(Fore.YELLOW)))
    clients = generateNodes(number_of_nodes=number_of_nodes)
    K = int(input("{0}What percentage of participating clients do you want?\n".format(Fore.YELLOW)))
    K = K / 100
    selected_clients = RandomClientSelection(nodes=clients, K=K, debug_mode=False).randomClientSelection()

    selected_clients_list = selected_to_dict(selected_clients)

    number_weak_nodes, number_mid_nodes, number_powerful_nodes = count_clients(selected_clients)

    print("{0}Selected clients are : ".format(Fore.MAGENTA))
    print("{0}---------------------------------------------------------".format(Fore.MAGENTA))
    print(selected_clients_list)
    print("{0}---------------------------------------------------------".format(Fore.MAGENTA))
    print("[*] {0}{1} ({2}%) clients has been selected".format(Fore.MAGENTA, len(selected_clients), K * 100))
    print("[*] {0} There is {1} Weak nodes".format(Fore.RED, number_weak_nodes))
    print("[*] {0} There is {1} Medium power nodes".format(Fore.YELLOW, number_mid_nodes))
    print("[*] {0} There is {1} Powerful nodes".format(Fore.GREEN, number_powerful_nodes))
