from utils.stats import count_clients, display_client_information, draw_graph, count_rejected_clients, show_results
from utils.generation import generateNodes, selected_to_dict, sampling_data_to_clients, choose_dataset
from constants.model_constants import NUM_CLASSES, NUM_CHANNELS
from distribuedLearning.DistribuedLearning import dist_learning
from clientSelection import RandomClientSelection
from constants.federated_learning import ROUNDS
from torchvision import datasets, transforms
from utils.displays import display_author
from models.CNN.CNNMnist import CNNMnist
from colorama import init, Fore
from tqdm import tqdm
import warnings


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
    train_loss, train_accuracy = [], []
    total_energy = 0

    for epoch in range(ROUNDS):
        print(f'\n | Global Training Round : {epoch + 1} |\n')

        global_model.train()

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

    # ! -------------------------------------------- Start Distributed Learning  ---------------------------------------

        # ? Begin training on each client.

        loss_avg, list_acc, clients_acc, energy = dist_learning(selected_clients=selected_clients,
                                                                train_dataset=train_dataset,
                                                                global_model=global_model,
                                                                global_round=epoch)

    train_accuracy.append(sum(list_acc) / len(list_acc))
    train_loss.append(loss_avg)
    total_energy = total_energy + energy

    # ! ---------------------------------------------------- End ! -----------------------------------------------------

    # ! ---------------------------------------------------- Results ---------------------------------------------------

    show_results() # ? Print loss and the accuracy of each node.

    method = "Vanila FL"

    number_rejected_clients = count_rejected_clients(clients)

    accuracy_data, energy_data, down_data = {method: 100 * train_accuracy[-1]}, {method: total_energy}, \
                                            {method: number_rejected_clients}

    draw_graph(accuracy_data=accuracy_data, energy_data=energy_data, down_data=down_data)

    # ! ---------------------------------------------------- End ! -----------------------------------------------------
