from utils.stats import count_clients, display_client_information, draw_graph, count_rejected_clients, show_results
from utils.generation import generateNodes, selected_to_dict, sampling_data_to_clients, choose_dataset, \
    split_nodes_networks
from constants.model_constants import NUM_CLASSES, NUM_CHANNELS
from distribuedLearning.DistribuedLearning import dist_learning
from clientSelection import LeaderClientSelection, RandomClientSelection
from constants.federated_learning import ROUNDS, FINAL_ACCURACY
from leaderElection.leaderElection import LeaderElection
from utils.displays import display_author
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
    display_author()  # * Display authors information

    # ! -------------------------------------------- Generation process ------------------------------------------------

    # ? Choose how many nodes you want to simulate.
    number_of_nodes = int(input("{0}How Many nodes do you want to simulate ?\n> ".format(Fore.LIGHTYELLOW_EX)))

    # ? Specify the percentage of choice of the participant clients.
    selection_percentage = int(input("{0}What percentage of participating clients do you want?\n> ".
                                     format(Fore.LIGHTYELLOW_EX))) / 100

    # ? Choosing the dataset ( 1 = MNIST, 2 = Fashion MNIST, 3 = CIFAR 100).
    dataset_id, train_dataset, test_dataset = choose_dataset()

    # ? Generate the number chosen of nodes.
    clients = generateNodes(number_of_nodes=number_of_nodes)
    # ? Split each number of nodes into a single network.
    networks = split_nodes_networks(nodes=clients)
    # ? Choose leader for each network.
    print("{0}[*] Choosing the leader of each network".format(Fore.LIGHTBLUE_EX))
    for network in networks:
        clients = network.get_nodes()
        leaderElection = LeaderElection(nodes=clients, debug_mode=False)
        leader = leaderElection.MinFind()
        network.set_network_leader(leader)
        print("{0}[+] The leader ID of network {1} is : {2} (ID = {3}, IP :{4})".format(Fore.LIGHTYELLOW_EX,
                                                                                        network.get_network_number(),
                                                                                        leader.get_name(),
                                                                                        leader.get_id(),
                                                                                        leader.get_ip_addr()))

    leader_selection = LeaderClientSelection(nodes=clients, K=0.1, networks=networks, debug_mode=False) \
        .gathering_process()

    exit(0)
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
        print("test")
        exit(0)

        # ! ---------------------------------------------------- End ! -----------------------------------------------------

        # ! -------------------------------------------- Start Distributed Learning  ---------------------------------------

        # ? Begin training on each client.

        loss_avg, list_acc, clients_acc, energy = dist_learning(selected_clients=selected_clients,
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

    show_results(train_loss=train_loss, clients_acc=clients_acc)  # ? Print loss and the accuracy of each node.

    method = "Leader-assisted Client selection"

    number_rejected_clients = count_rejected_clients(clients)

    accuracy_data, energy_data, down_data = {method: 100 * train_accuracy[-1]}, \
                                            {method: total_energy}, \
                                            {method: number_rejected_clients}

    draw_graph(accuracy_data=accuracy_data, energy_data=energy_data, down_data=down_data)

    # ! ---------------------------------------------------- End ! -----------------------------------------------------
