from utils.stats import count_clients, display_client_information, draw_graph, count_rejected_clients, show_results
from utils.generation import generate_nodes, selected_to_dict, choose_dataset, split_nodes_networks
from constants.model_constants import NUM_CLASSES, NUM_CHANNELS
from distributedLearning.DistributedLearning import dist_learning
from clientSelection import LeaderClientSelection
from constants.federated_learning import ROUNDS, FINAL_ACCURACY
from leaderElection.LeaderElection import LeaderElection
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

# TODO: Changing sampling data function.

# TODO : Fix IPs.

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
    clients = generate_nodes(number_of_nodes=number_of_nodes, data=train_dataset)
    # ? Split each number of nodes into a single network.
    networks = split_nodes_networks(nodes=clients)
    # ? Choose leader for each network.
    print("{0}[*] Choosing the leader of each network".format(Fore.LIGHTBLUE_EX))
    for network in networks:
        leader = LeaderElection(nodes=network.get_nodes(), debug_mode=False).min_find()
        network.set_network_leader(leader)
        print("{0}[+] The leader ID of network {1} is : {2} (ID = {3}, IP :{4})".format(Fore.LIGHTYELLOW_EX,
                                                                                        network.get_network_number(),
                                                                                        leader.get_name(),
                                                                                        leader.get_id(),
                                                                                        leader.get_ip_addr()))
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
        # ? Gathering Process.
        LeaderClientSelection(nodes=clients, K=selection_percentage, networks=networks, debug_mode=False) \
            .gathering_process()

        # ? Call Leader client selection module to select eligible clients.
        selected_clients = LeaderClientSelection(nodes=clients, K=selection_percentage, networks=networks,
                                                 debug_mode=False).leader_client_selection()

        # ? Convert the output of random clients to list.
        selected_clients_list = selected_to_dict(selected_clients=selected_clients)

        # ? Get the number of weak, mid and powerful nodes.
        number_weak_nodes, number_mid_nodes, number_powerful_nodes = count_clients(selected_clients=selected_clients)

        # ? Display some stats about selected clients.
        display_client_information(selected_clients_list=selected_clients_list, selected_clients=selected_clients,
                                   number_weak_nodes=number_weak_nodes, number_mid_nodes=number_mid_nodes,
                                   number_powerful_nodes=number_powerful_nodes, K=selection_percentage)

    # ! -------------------------------------------- End of client selection process -----------------------------------

    # ! -------------------------------------------- Start Distributed Learning  ---------------------------------------

        # ? Begin training on each client.

        loss_avg, list_acc, clients_acc, energy = dist_learning(train_dataset=train_dataset,
                                                                selected_clients=selected_clients,
                                                                global_model=global_model, global_round=epoch)

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