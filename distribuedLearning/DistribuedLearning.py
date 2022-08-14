import copy
from colorama import Fore
from models.update import ClientUpdate
from utils.computation import average_weights


def dist_learning(train_dataset, selected_clients: list, global_model, global_round: int) -> (float, list, dict, float):
    local_weights, local_losses = [], []
    energy = 0
    index = 1

    for client in selected_clients:  # ? For each client in the selected clients.

        if client.getStatus() == 0:  # ? Check the status of client it's down or not.
            print("{0}[-] {1} is down, Skipping ..".format(Fore.RED, client.getName()))
            index += 1
            continue

        print("{0}Client Nº{1} [Round {2}] -  Begin training with {3} ({4} ( Data length : {5})".
              format(Fore.CYAN,
                     index,
                     global_round + 1,
                     client.getName(),
                     client.getId(),
                     len(client.getData())))

        local_model = ClientUpdate(dataset=train_dataset, idxs=client.getData(), node=client)

        results = local_model.updateWeights(model=copy.deepcopy(global_model), global_round=global_round)

        if results is None:  # ? if the client is down.
            print("{0}[-] {1} is down, Skipping ..".format(Fore.RED, client.getName()))
            index += 1
            continue

        local_weight, local_loss, local_energy = results

        energy = energy + local_energy

        local_weights.append(copy.deepcopy(local_weight))

        local_losses.append(copy.deepcopy(local_loss))

        # ? if the node is on battery mode.
        battery_percent = (client.getCurrentEnergy() / client.getTotalEnergy()) * 100 \
            if client.getTotalEnergy() is not None else 100

        # ? Calculate the percentage of storage.
        storage_percent = (client.getCurrentStorage() / client.getTotalStorage()) * 100

        memory_usage = client.getMemoryUsage()

        cpu_usage = client.getCpuUsage()

        print("{}Learning is complete for {} (Battery : {:.1f}%, Storage : {:.1f}%, Memory : {:.1f}%, CPU : {:.1f}%)"
              .format(Fore.GREEN, client.getName(),
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
        local_model = ClientUpdate(dataset=train_dataset, idxs=client.getData(), node=client)
        acc, loss = local_model.inference(model=global_model)
        clients_acc[client.getName()] = "{:.2f}%".format(100 * acc)
        list_acc.append(acc)
        list_loss.append(loss)

    return loss_avg, list_acc, clients_acc, energy
