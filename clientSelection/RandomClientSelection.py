import random
from colorama import Fore, Style
from clientSelection.ClientSelection import ClientSelection


class RandomClientSelection(ClientSelection):
    def __init__(self, nodes: list, K: float = 0.1, debug_mode: bool = False):
        super().__init__(nodes, debug_mode)
        self.K = K
        self.debug_mode = debug_mode

    def random_client_selection(self) -> list:
        print("{0}[*] Starting Random client selection".format(Fore.LIGHTYELLOW_EX))
        selected_clients = []
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
            selected_clients.append(client)

        return selected_clients
