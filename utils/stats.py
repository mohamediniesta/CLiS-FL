from node import PowNode, MidNode, LowNode


def count_clients(selected_clients: list) -> (int, int, int):
    number_weak_nodes = 0
    number_mid_nodes = 0
    number_powerful_nodes = 0

    for client in selected_clients:
        if isinstance(client, LowNode):
            number_weak_nodes = number_weak_nodes + 1
        if isinstance(client, MidNode):
            number_mid_nodes = number_mid_nodes + 1
        if isinstance(client, PowNode):
            number_powerful_nodes = number_powerful_nodes + 1

    return number_weak_nodes, number_mid_nodes, number_powerful_nodes
