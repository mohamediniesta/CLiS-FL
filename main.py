from colorama import init, Fore
from utils.generation import generateNodes, selected_to_dict
from utils.stats import count_clients, display_client_information
from ClientSelection import RandomClientSelection

init(autoreset=True)

if __name__ == '__main__':
    # Client generation and selection process.
    number_of_nodes = int(input("{0}How Many nodes do you want to simulate ?\n".format(Fore.YELLOW)))
    clients = generateNodes(number_of_nodes=number_of_nodes)
    K = int(input("{0}What percentage of participating clients do you want?\n".format(Fore.YELLOW)))
    K = K / 100
    selected_clients = RandomClientSelection(nodes=clients, K=K, debug_mode=False).randomClientSelection()

    selected_clients_list = selected_to_dict(selected_clients=selected_clients)

    number_weak_nodes, number_mid_nodes, number_powerful_nodes = count_clients(selected_clients=selected_clients)
    # Display some stats about selected clients.
    display_client_information(selected_clients_list=selected_clients_list, selected_clients=selected_clients,
                               number_weak_nodes=number_weak_nodes, number_mid_nodes=number_mid_nodes,
                               number_powerful_nodes=number_powerful_nodes, K=K)
    # Choosing the dataset.
    datasets = {1: "mnist", 2: "fashion_mnist", 3: "cifar"}
    dataset_id = int(input('''{0}Which dataset do you want to use ?
1 - Mnist  
2 - Fashion Mnist 
3 - Cifar\n'''.format(Fore.YELLOW)))

    dataset = datasets[dataset_id]
