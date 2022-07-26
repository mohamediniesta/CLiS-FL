import random
from colorama import Fore, Style
from time import sleep
from network.Network import Network
from clientSelection.ClientSelection import ClientSelection


class LeaderClientSelection(ClientSelection):
    def __init__(self, nodes: list, networks: list, K: float = 0.1, debug_mode: bool = False):
        super().__init__(nodes, debug_mode)
        self.networks = networks
        self.K = K
        self.debug_mode = debug_mode

    def gathering_process(self):
        print("{0}[*] Start Gathering Process !!!".format(Fore.LIGHTBLUE_EX))
        for i in range(0, 7):
            for network in self.networks:
                leader = network.get_network_leader()
                clients = network.get_nodes()
                for client in clients:
                    rsrc_info = client.get_resources_information()
                    leader_data = leader.get_gathered_data()
                    leader.set_gathered_data(leader_data + rsrc_info)
            sleep(120)

    def leaderClientSelection(self) -> list:
        selectedClients = []
        percentage = round(len(self.nodes) * self.K)
        for i in range(0, percentage):
            client = random.choices(self.nodes)[0]
            if self.debug_mode:
                print(
                    "[*] The client {0}{1}{2} with id : {3}{4},{5} has been selected".format(Fore.YELLOW,
                                                                                             client.get_name(),
                                                                                             Style.RESET_ALL,
                                                                                             Fore.MAGENTA,
                                                                                             client.get_id(),
                                                                                             Style.RESET_ALL))
            selectedClients.append(client)

        return selectedClients
