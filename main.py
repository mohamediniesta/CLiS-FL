import copy
from colorama import init, Fore
from utils.generation import generateNodes, selected_to_dict, sampling_data_to_clients
from utils.stats import count_clients, display_client_information
from utils.computation import average_weights
from ClientSelection import RandomClientSelection
from torchvision import datasets, transforms
from Models.CNN.CNNMnist import CNNMnist
from update import LocalUpdate
import numpy as np


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

    device = 'cuda' if gpu_mode else 'cpu'

    global_model = CNNMnist(num_channels=1, num_classes=10)
    global_model.to(device)
    global_model.train()

    local_weights, local_losses = [], []
    train_loss, train_accuracy = [], []
    for client in selected_clients:
        print("Begin training with {}".format(client.get_name()))
        local_model = LocalUpdate(dataset=train_dataset,
                                  idxs=client.get_data())
        w, loss = local_model.update_weights(
            model=copy.deepcopy(global_model), global_round=1)
        local_weights.append(copy.deepcopy(w))
        local_losses.append(copy.deepcopy(loss))

    global_weights = average_weights(local_weights)
    global_model.load_state_dict(global_weights)
    loss_avg = sum(local_losses) / len(local_losses)
    train_loss.append(loss_avg)
    print(f'Training Loss : {np.mean(np.array(train_loss))}')

    exit(0)
