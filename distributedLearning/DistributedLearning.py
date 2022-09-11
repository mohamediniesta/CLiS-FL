# pylint: disable = C0114, C0115, C0116, C0103

import copy
from colorama import Fore
from models.update import ClientUpdate
from utils.computation import average_weights


def dist_learning(train_dataset, selected_clients: list, global_model, global_round: int) \
        -> (float, list, dict, float):
    """
    The function of distributed learning of nodes.

    Parameters
    ----------
        train_dataset : any
            The training dataset used for distributed learning.
        selected_clients : list
            The selected clients.
        global_model : any
            The model global.
        global_round : int
            The current global round.

    Returns
    -------
        loss_avg (float): the avereage loss.
        list_acc (list): the full list of all accuracy.
        clients_acc (dict) : the full list of clients accuracy as dict format.
        energy (float) : The total energy consumed during distributed learning.

    Examples
    --------
    >>> loss_avg, list_acc, clients_acc, energy = dist_learning(train_dataset=train_dataset, \
    selected_clients=selected_clients, global_model=global_model, global_round=epoch)
    """
    local_weights, local_losses = [], []
    energy = 0
    index = 1

    for client in selected_clients:  # ? For each client in the selected clients.

        if client.get_status() == 0:  # ? Check the status of client it's down or not.
            print(f"{Fore.RED}[-] {client.get_name()} is down, Skipping ..")
            index += 1
            continue

        print(f"{Fore.CYAN}Client Nº{index} [Round {global_round + 1}] -  "
              f"Begin training with {client.get_name()} ({client.get_id()} "
              f"( Data length : {len(client.get_data())})")
        local_model = ClientUpdate(dataset=train_dataset, idxs=client.get_data(), node=client)

        results = local_model.update_weights(model=copy.deepcopy(global_model),
                                             global_round=global_round)

        if results is None:
            # ? if the client is down.
            print(f"{Fore.RED}Learning not completed ! [-] "
                  f"{client.get_name()} is down, Skipping ..")
            index += 1
            continue

        local_weight, local_loss, local_energy = results

        energy = energy + local_energy

        local_weights.append(copy.deepcopy(local_weight))

        local_losses.append(copy.deepcopy(local_loss))

        # ? if the node is on battery mode.
        battery_percent = (client.get_current_energy() / client.get_total_energy()) * 100 \
            if client.get_total_energy() is not None else 100

        # ? Calculate the percentage of storage.
        storage_percent = (client.get_current_storage() / client.get_total_storage()) * 100

        memory_usage = client.get_memory_usage()

        cpu_usage = client.get_cpu_usage()

        print(f"{Fore.GREEN}Learning is complete for {client.get_name()} "
              f"(Battery : {battery_percent:.1f}%, "
              f"Storage : {storage_percent:.1f}%, "
              f"Memory : {memory_usage:.1f}%,"
              f" CPU : {cpu_usage:.1f}%)")
        index += 1

    if len(local_weights) > 0:
        print(f"{Fore.LIGHTGREEN_EX}[*] Aggregation ")
        global_weights = average_weights(local_weights)  # ? Model's aggregation.
        global_model.load_state_dict(global_weights)
        loss_avg = sum(local_losses) / len(local_losses)
    else:
        loss_avg = None

    # ? Inference Phase (Test our model on test data).

    list_acc, list_loss = [], []
    global_model.eval()
    clients_acc = {}

    for client in selected_clients:
        local_model = ClientUpdate(dataset=train_dataset, idxs=client.get_data(), node=client)
        acc, loss = local_model.inference(model=global_model)
        clients_acc[client.get_name()] = f"{100 * acc:.2f}%"
        list_acc.append(acc)
        list_loss.append(loss)

    return loss_avg, list_acc, clients_acc, energy
