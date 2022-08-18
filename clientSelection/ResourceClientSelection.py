from colorama import Fore
from clientSelection.ClientSelection import ClientSelection
import pandas as pd


class ResourceClientSelection(ClientSelection):
    # ? Select clients according to their resources. (The top ones with average power)
    def __init__(self, nodes: list, K: float = 0.1, debug_mode: bool = False):
        super().__init__(nodes, debug_mode)
        self.K = K
        self.debug_mode = debug_mode

    def resource_client_selection(self) -> list:
        print("{0}[*] Starting client selection by resources".format(Fore.LIGHTYELLOW_EX))
        selected_clients = []
        percentage = len(self.nodes) * self.K

        for node in self.nodes:
            # ? Collect the node's resources.
            rsrc_info = node.get_resources_information()
            name, cpu_power, cpu_usage, memory, memory_usage, total_storage, current_storage, battery_usage, \
            total_energy, energy_consumption, current_energy, data_length, date = rsrc_info

            data = {"Node": node, "Name": name, "cpu_power": cpu_power, "cpu_usage": cpu_usage,
                    "memory": memory, "memory_usage": memory_usage, "total_storage": total_storage,
                    "current_storage": current_storage, "battery_usage": battery_usage,
                    "total_energy": total_energy, "energy_consumption": energy_consumption,
                    "current_energy": current_energy, "data_length": data_length, "Date": date}
            # ? Put collected resources on DataFrame.
            resource_df = pd.concat([resource_df, pd.DataFrame.from_records([data])])

            resource_df['avg_power'] = resource_df[['total_energy', 'total_storage', 'cpu_power', 'memory']].mean(
                axis=1)
            # ? The top ones with average power
            selected_nodes = resource_df.nlargest(n=percentage, columns=['avg_power']).Node.values
            for client in selected_nodes:
                selected_clients.append(client)

        return selected_clients
