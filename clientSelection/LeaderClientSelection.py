from colorama import Fore, Style
from clientSelection.ClientSelection import ClientSelection
import pandas as pd


class LeaderClientSelection(ClientSelection):
    def __init__(self, nodes: list, networks: list, K: float = 0.1, debug_mode: bool = False):
        super().__init__(nodes, debug_mode)
        self.networks = networks
        self.K = K
        self.debug_mode = debug_mode

    def gathering_process(self):
        print("{0}[*] Start Gathering Process !!!".format(Fore.LIGHTBLUE_EX))
        for network in self.networks:
            leader = network.get_network_leader()
            df = pd.DataFrame()
            clients = network.get_nodes()
            for i in range(0, 7):
                for client in clients:
                    rsrc_info = client.get_resources_information()
                    name, cpu_power, cpu_usage, memory, memory_usage, total_storage, current_storage, battery_usage, \
                    total_energy, energy_consumption, current_energy, data_length, date = rsrc_info

                    data = {"Node": client, "Name": name, "cpu_power": cpu_power, "cpu_usage": cpu_usage,
                            "memory": memory, "memory_usage": memory_usage, "total_storage": total_storage,
                            "current_storage": current_storage, "battery_usage": battery_usage,
                            "total_energy": total_energy, "energy_consumption": energy_consumption,
                            "current_energy": current_energy, "data_length": data_length, "Date": date}
                    df = pd.concat([df, pd.DataFrame.from_records([data])])

            leader.set_gathered_data(gathered_data=df)

    def leader_client_selection(self) -> list:
        print("{0}[*] Starting Leader-assisted client selection".format(Fore.LIGHTYELLOW_EX))
        selected_clients = []
        percentage = len(self.nodes) * self.K

        for network in self.networks:
            leader = network.get_network_leader()
            leader_data = leader.get_gathered_data()
            leader_data['avg_power'] = leader_data[['total_energy', 'total_storage', 'cpu_power', 'memory']].mean(
                axis=1)
            local_percentage = int(percentage / len(self.networks))
            selected_nodes = leader_data.nlargest(n=local_percentage, columns=['avg_power']).Node.values
            for node in selected_nodes:
                selected_clients.append(node)

        return selected_clients
