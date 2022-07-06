from utils.generation import generateNodes, selected_to_dict, sampling_data_to_clients, choose_dataset
from utils.stats import count_clients, display_client_information, draw_graph, count_rejected_clients
from constants.model_constants import NUM_CLASSES, NUM_CHANNELS
from ClientSelection import RandomClientSelection
from utils.computation import average_weights
from torchvision import datasets, transforms
from utils.displays import display_author
from Models.CNN.CNNMnist import CNNMnist
from Models.update import LocalUpdate
from colorama import init, Fore
import numpy as np
import warnings
import copy

warnings.filterwarnings("ignore", category=DeprecationWarning)
init(autoreset=True)

if __name__ == '__main__':

    display_author()  # * Display authors information

    # ! -------------------------------------------- Generation process ------------------------------------------------

    # ? Choose how many nodes you want to simulate.
    number_of_nodes = int(input("{0}How Many nodes do you want to simulate ?\n".format(Fore.YELLOW)))

    # ? Specify the percentage of choice of the participant clients.
    selection_percentage = int(input("{0}What percentage of participating clients do you want?\n".
                                     format(Fore.YELLOW))) / 100

    # ? Choosing the dataset.
    # dataset = choose_dataset()

    # ? Apply transform and splitting datasets intro train and test.
    apply_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    PATH = "datasets/mnist/"
    train_dataset = datasets.MNIST(PATH, train=True, download=True, transform=apply_transform)
    test_dataset = datasets.MNIST(PATH, train=False, download=True, transform=apply_transform)

    # ? Generate the number chosen of nodes.
    clients = generateNodes(number_of_nodes=number_of_nodes)

    # ! ---------------------------------------------------- End ! -----------------------------------------------------

    # ! -------------------------------------------- Generic Model ----------------------------------------------------

    global_model = CNNMnist(num_channels=NUM_CHANNELS, num_classes=NUM_CLASSES)

    global_model.train()  # ? Generic model.

    global_weights = global_model.state_dict()

    # ! ---------------------------------------------------- End ! -----------------------------------------------------

    # ! -------------------------------------------- Client selection process ------------------------------------------
    # ? Call Random client selection module to select random clients.
    selected_clients = RandomClientSelection(nodes=clients, K=selection_percentage,
                                             debug_mode=False).randomClientSelection()

    # ? Convert the output of random clients to list.
    selected_clients_list = selected_to_dict(selected_clients=selected_clients)

    # ? Get the number of weak, mid and powerful nodes.
    number_weak_nodes, number_mid_nodes, number_powerful_nodes = count_clients(selected_clients=selected_clients)

    # ? Display some stats about selected clients.
    display_client_information(selected_clients_list=selected_clients_list, selected_clients=selected_clients,
                               number_weak_nodes=number_weak_nodes, number_mid_nodes=number_mid_nodes,
                               number_powerful_nodes=number_powerful_nodes, K=selection_percentage)

    # ! -------------------------------------------- End of client selection process -----------------------------------

    # ! -------------------------------------------- Dataset, Encoding, Sampling  --------------------------------------

    # ? Split dataset into the clients.
    sampling_data_to_clients(data=train_dataset, selected_client=selected_clients)

    # ! ---------------------------------------------------- End ! -----------------------------------------------------

    # ! -------------------------------------------- Start Federated Learning  -----------------------------------------

    # ? Begin training on each client.

    local_weights, local_losses = [], []
    train_loss, train_accuracy = [], []
    total_energy = 0
    i = 1
    for client in selected_clients:  # ? For each client in the selected clients.
        if client.get_status() == 0:  # ? Check the status of client it's down or not.
            print("{0}[-] {1} is down, Skipping ..".format(Fore.RED, client.get_name()))
            i = i + 1
            continue
        print(
            "{0}Client Nº{1} -  Begin training with {2} ({3})".format(Fore.CYAN, i, client.get_name(), client.get_id()))
        local_model = LocalUpdate(dataset=train_dataset, idxs=client.get_data(), node=client)
        w, loss, e = local_model.update_weights(
            model=copy.deepcopy(global_model), global_round=1)
        total_energy = total_energy + e
        local_weights.append(copy.deepcopy(w))
        local_losses.append(copy.deepcopy(loss))
        if client.get_total_energy() is not None:  # ? if the node is on battery mode.
            # ? Calculate the percentage of battery.
            battery_p = (client.get_current_energy() / client.get_total_energy()) * 100
        else:
            battery_p = 100
        # ? Calculate the percentage of storage.
        storage_p = (client.get_current_storage() / client.get_total_storage()) * 100
        print(
            "{}Learning is complete for {} (Battery : {:.1f}%, Storage : {:.1f}%)".format(Fore.GREEN, client.get_name(),
                                                                                          battery_p, storage_p))
        i = i + 1

    global_weights = average_weights(local_weights)  # ? Model's aggregation.
    global_model.load_state_dict(global_weights)
    loss_avg = sum(local_losses) / len(local_losses)
    train_loss.append(loss_avg)

    list_acc, list_loss = [], []
    global_model.eval()
    clients_acc = {}

    for client in selected_clients:
        local_model = LocalUpdate(dataset=train_dataset, idxs=client.get_data(), node=client)
        acc, loss = local_model.inference(model=global_model)
        clients_acc[client.get_name()] = "{:.2f}%".format(100 * acc)
        list_acc.append(acc)
        list_loss.append(loss)
    train_accuracy.append(sum(list_acc) / len(list_acc))

    # ! ---------------------------------------------------- End ! -----------------------------------------------------

    print("-" * 30)
    print('Global Training Accuracy: {:.2f}% \n'.format(100 * train_accuracy[-1]))
    print(f'Global Training Loss : {np.mean(np.array(train_loss))}')
    print("Local accuracy of each client : ")
    print("-" * 30)
    print(clients_acc)
    print("-" * 30)
    method = "Vanila FL"
    number_rejected_clients = count_rejected_clients(clients)
    accuracy_data = {method: 100 * train_accuracy[-1]}
    energy_data = {method: total_energy}
    down_data = {method: number_rejected_clients}

    draw_graph(accuracy_data=accuracy_data, energy_data=energy_data, down_data=down_data)
