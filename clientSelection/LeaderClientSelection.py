import random
from colorama import Fore, Style
from time import sleep
from clientSelection.ClientSelection import ClientSelection
import pandas as pd


class LeaderClientSelection(ClientSelection):
    def __init__(self, nodes: list, networks: list, K: float = 0.1, debug_mode: bool = False):
        super().__init__(nodes, debug_mode)
        self.networks = networks
        self.K = K
        self.debug_mode = debug_mode

    def GatheringProcess(self):
        print("{0}[*] Start Gathering Process !!!".format(Fore.LIGHTBLUE_EX))
        for network in self.networks:
            leader = network.getNetworkLeader()
            df = pd.DataFrame()
            clients = network.getNodes()
            for i in range(0, 7):
                for client in clients:
                    rsrc_info = client.getResourcesInformation()
                    name, cpu_power, cpu_usage, memory, memory_usage, total_storage, current_storage, battery_usage, \
                    total_energy, energy_consumption, current_energy, data_length, date = rsrc_info

                    data = {"Node": client, "Name": name, "cpu_power": cpu_power, "cpu_usage": cpu_usage,
                            "memory": memory, "memory_usage": memory_usage, "total_storage": total_storage,
                            "current_storage": current_storage, "battery_usage": battery_usage,
                            "total_energy": total_energy, "energy_consumption": energy_consumption,
                            "current_energy": current_energy, "data_length": data_length, "Date": date}
                    df = pd.concat([df, pd.DataFrame.from_records([data])])

            leader.setGatheredData(gathered_data=df)

    def leaderClientSelection(self) -> list:
        selectedClients = []
        percentage = len(self.nodes) * self.K

        for network in self.networks:
            leader = network.getNetworkLeader()
            leader_data = leader.getGatheredData()
            leader_data['avg_power'] = leader_data[['total_energy', 'total_storage', 'cpu_power', 'memory']].mean(
                axis=1)
            local_percentage = int(percentage / len(self.networks))
            selected_nodes = leader_data.nlargest(n=local_percentage, columns=['avg_power']).Node.values
            for node in selected_nodes:
                selectedClients.append(node)

        return selectedClients
