import copy
from colorama import Fore
from models.update import ClientUpdate
from utils.computation import average_weights


def dist_learning(train_dataset, selected_clients: list, global_model, global_round: int) -> (float, list, dict, float):
    local_weights, local_losses = [], []
    energy = 0
    index = 1

    for client in selected_clients:  # ? For each client in the selected clients.

        if client.get_status() == 0:  # ? Check the status of client it's down or not.
            print("{0}[-] {1} is down, Skipping ..".format(Fore.RED, client.get_name()))
            index += 1
            continue

        print("{0}Client Nº{1} [Round {2}] -  Begin training with {3} ({4} ( Data length : {5})".
              format(Fore.CYAN,
                     index,
                     global_round + 1,
                     client.get_name(),
                     client.get_id(),
                     len(client.get_data())))

        local_model = ClientUpdate(dataset=train_dataset, idxs=client.get_data(), node=client)

        results = local_model.update_weights(model=copy.deepcopy(global_model), global_round=global_round)

        if results is None:  # ? if the client is down.
            print("{0}[-] {1} is down, Skipping ..".format(Fore.RED, client.get_name()))
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

        print("{}Learning is complete for {} (Battery : {:.1f}%, Storage : {:.1f}%, Memory : {:.1f}%, CPU : {:.1f}%)"
              .format(Fore.GREEN, client.get_name(),
                      battery_percent, storage_percent, memory_usage, cpu_usage))
        index += 1

    global_weights = average_weights(local_weights)  # ? Model's aggregation.
    global_model.load_state_dict(global_weights)
    loss_avg = sum(local_losses) / len(local_losses)

    list_acc, list_loss = [], []
    global_model.eval()
    clients_acc = {}

    # ? Inference Phase (Test our model on test data).

    for client in selected_clients:
        local_model = ClientUpdate(dataset=train_dataset, idxs=client.get_data(), node=client)
        acc, loss = local_model.inference(model=global_model)
        clients_acc[client.get_name()] = "{:.2f}%".format(100 * acc)
        list_acc.append(acc)
        list_loss.append(loss)

    return loss_avg, list_acc, clients_acc, energy
