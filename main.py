import copy
from colorama import init, Fore
from utils.generation import generateNodes, selected_to_dict, sampling_data_to_clients
from utils.stats import count_clients, display_client_information
from utils.computation import average_weights
from ClientSelection import RandomClientSelection
from torchvision import datasets, transforms
from Models.CNN.CNNMnist import CNNMnist
from Models.update import LocalUpdate
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

init(autoreset=True)

if __name__ == '__main__':
    print("""{}
  ______ _                  _____ _                 _       _   _             
 |  ____| |                / ____(_)               | |     | | (_)            
 | |__  | |       ______  | (___  _ _ __ ___  _   _| | __ _| |_ _  ___  _ __  
 |  __| | |      |______|  \___ \| | '_ ` _ \| | | | |/ _` | __| |/ _ \| '_ \ 
 | |    | |____            ____) | | | | | | | |_| | | (_| | |_| | (_) | | | |
 |_|    |______|          |_____/|_|_| |_| |_|\__,_|_|\__,_|\__|_|\___/|_| |_|
                                                                              """.format(Fore.CYAN))
    print("{}🤖 {}By AICHE Mohamed".format(Fore.YELLOW, Fore.MAGENTA))
    print(Fore.MAGENTA + "-" * 20)
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

    # exit(0)
    # Choosing the dataset.
    dataset_list = {1: "mnist", 2: "fashion_mnist", 3: "cifar"}
    dataset_id = int(input('''{0}Which dataset do you want to use ?
1 - Mnist  
2 - Fashion Mnist 
3 - Cifar\n'''.format(Fore.YELLOW)))

    dataset = dataset_list[dataset_id]

    apply_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))])

    train_dataset = datasets.MNIST("datasets/mnist/", train=True, download=True,
                                   transform=apply_transform)

    test_dataset = datasets.MNIST("datasets/mnist/", train=False, download=True,
                                  transform=apply_transform)

    sampling_data_to_clients(train_dataset, selected_clients)

    gpu_mode = False

    global_model = CNNMnist(num_channels=1, num_classes=10)

    global_model.train()

    local_weights, local_losses = [], []
    train_loss, train_accuracy = [], []
    i = 1
    for client in selected_clients:
        if client.get_status() == 0:
            print("{0}[-] {1} is down, Skipping ..".format(Fore.RED, client.get_name()))
            i = i + 1
            continue
        print("{0}Client Nº{1} -  Begin training with {2} ({3})".format(Fore.CYAN, i, client.get_name(), client.get_id()))
        local_model = LocalUpdate(dataset=train_dataset, idxs=client.get_data(), node=client)
        w, loss = local_model.update_weights(
            model=copy.deepcopy(global_model), global_round=1)
        local_weights.append(copy.deepcopy(w))
        local_losses.append(copy.deepcopy(loss))
        if client.get_total_energy() is not None:
            battery_p = (client.get_current_energy() / client.get_total_energy()) * 100
        else:
            battery_p = 100
        storage_p = (client.get_current_storage() / client.get_total_storage()) * 100
        print("{}Learning is complete for {} (Battery : {:.1f}%, Storage : {:.1f}%)".format(Fore.GREEN, client.get_name(),
              battery_p, storage_p))
        i = i + 1

    global_weights = average_weights(local_weights)
    global_model.load_state_dict(global_weights)
    loss_avg = sum(local_losses) / len(local_losses)
    train_loss.append(loss_avg)
    print(f'Training Loss : {np.mean(np.array(train_loss))}')

    exit(0)
