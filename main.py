from utils.stats import countClients, displayClientInformation, drawGraph, countRejectedClients, showResults
from utils.generation import generateNodes, selectedToDict, dataDistribution, chooseDataset
from constants.model_constants import NUM_CLASSES, NUM_CHANNELS
from distribuedLearning.DistribuedLearning import distLearning
from clientSelection import RandomClientSelection
from constants.federated_learning import ROUNDS, FINAL_ACCURACY
from utils.displays import displayAuthor
from models.CNN.CNNMnist import CNNMnist
from models.CNN.CNNCifar import CNNCifar
from colorama import init, Fore
from time import sleep
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
init(autoreset=True)

# TODO : Optimize Battery Modeling.

# TODO : Adding noise process to clients randomly.

# TODO: Generating sphinx documentations.

if __name__ == '__main__':
    displayAuthor()  # * Display authors information

    # ! -------------------------------------------- Generation process ------------------------------------------------

    # ? Choose how many nodes you want to simulate.
    number_of_nodes = int(input("{0}How Many nodes do you want to simulate ?\n> ".format(Fore.LIGHTYELLOW_EX)))

    # ? Specify the percentage of choice of the participant clients.
    selection_percentage = int(input("{0}What percentage of participating clients do you want?\n> ".
                                     format(Fore.LIGHTYELLOW_EX))) / 100

    # ? Choosing the dataset ( 1 = MNIST, 2 = Fashion MNIST, 3 = CIFAR 100).
    dataset_id, train_dataset, test_dataset = chooseDataset()

    # ? Generate the number chosen of nodes.
    clients = generateNodes(number_of_nodes=number_of_nodes)

    # ! ---------------------------------------------------- End ! -----------------------------------------------------

    # ! -------------------------------------------- Generic Model ----------------------------------------------------
    global_model = CNNCifar() if dataset_id == 3 else CNNMnist(num_channels=NUM_CHANNELS, num_classes=NUM_CLASSES)

    global_model.train()  # ? Generic model.

    global_weights = global_model.state_dict()

    # ! ---------------------------------------------------- End ! -----------------------------------------------------
    train_loss, train_accuracy = [], []
    total_energy = 0

    for epoch in range(ROUNDS):
        print("\n{0}Global Training Round : {1}\n".format(Fore.LIGHTYELLOW_EX, epoch + 1))

        sleep(2)

        global_model.train()

    # ! -------------------------------------------- Client selection process ------------------------------------------
        # ? Call Random client selection module to select random clients.
        selected_clients = RandomClientSelection(nodes=clients, K=selection_percentage,
                                                 debug_mode=False).randomClientSelection()

        # ? Convert the output of random clients to list.
        selected_clients_list = selectedToDict(selected_clients=selected_clients)

        # ? Get the number of weak, mid and powerful nodes.
        number_weak_nodes, number_mid_nodes, number_powerful_nodes = countClients(selected_clients=selected_clients)

        # ? Display some stats about selected clients.
        displayClientInformation(selected_clients_list=selected_clients_list, selected_clients=selected_clients,
                                 number_weak_nodes=number_weak_nodes, number_mid_nodes=number_mid_nodes,
                                 number_powerful_nodes=number_powerful_nodes, K=selection_percentage)

    # ! -------------------------------------------- End of client selection process -----------------------------------

    # ! -------------------------------------------- Dataset, Encoding, Sampling  --------------------------------------

        # ? Split dataset into the clients.
        dataDistribution(data=train_dataset, selected_client=selected_clients)

    # ! ---------------------------------------------------- End ! -----------------------------------------------------

    # ! -------------------------------------------- Start Distributed Learning  ---------------------------------------

        # ? Begin training on each client.

        loss_avg, list_acc, clients_acc, energy = distLearning(selected_clients=selected_clients,
                                                               train_dataset=train_dataset,
                                                               global_model=global_model,
                                                               global_round=epoch)

        global_acc = sum(list_acc) / len(list_acc)

        print("Global accuracy : {0} %".format(global_acc * 100))

        train_accuracy.append(global_acc)
        train_loss.append(loss_avg)
        total_energy = total_energy + energy

        if global_acc >= FINAL_ACCURACY / 100:
            print("{0}[+] Global accuracy reached !! No more rounds for FL".format(Fore.LIGHTGREEN_EX))
            break

    # ! ---------------------------------------------------- End ! -----------------------------------------------------

    # ! ---------------------------------------------------- Results ---------------------------------------------------

    showResults(train_loss=train_loss, clients_acc=clients_acc)  # ? Print loss and the accuracy of each node.

    method = "Vanila FL"

    number_rejected_clients = countRejectedClients(clients)

    accuracy_data, energy_data, down_data = {method: 100 * train_accuracy[-1]}, \
                                            {method: total_energy}, \
                                            {method: number_rejected_clients}

    drawGraph(accuracy_data=accuracy_data, energy_data=energy_data, down_data=down_data)

    # ! ---------------------------------------------------- End ! -----------------------------------------------------
