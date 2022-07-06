from models.update import LocalUpdate
from utils.computation import average_weights
from colorama import Fore
import copy


def dist_learning(train_dataset, selected_clients: list, global_model, global_round):
    local_weights, local_losses = [], []
    energy = 0
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
            model=copy.deepcopy(global_model), global_round=global_round)
        energy = energy + e
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

    list_acc, list_loss = [], []
    global_model.eval()
    clients_acc = {}

    for client in selected_clients:
        local_model = LocalUpdate(dataset=train_dataset, idxs=client.get_data(), node=client)
        acc, loss = local_model.inference(model=global_model)
        clients_acc[client.get_name()] = "{:.2f}%".format(100 * acc)
        list_acc.append(acc)
        list_loss.append(loss)

    return loss_avg, list_acc, clients_acc, energy
