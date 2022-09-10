# pylint: disable = C0114, C0115, C0116, C0103

import random
from colorama import Fore, Style
from clientSelection.ClientSelection import ClientSelection


class RandomClientSelection(ClientSelection):
    """
     A class that inherits the client selection module, which selects clients randomly.

     ...

     Attributes
     ----------
     nodes : list
         The list of all nodes in the environment.
     K : float
         the percentage of the selection.
     debug_mode : bool
         Indicates if the debug mode is enabled or not.

     Methods
     -------
     random_client_selection():
         Returns a randomly selected list of clients with a percentage K.

     """

    def __init__(self, nodes: list, K: float = 0.1, debug_mode: bool = False):
        """
        Constructs all the necessary attributes for the RandomClientSelection object.

        Parameters
        ----------
            nodes : list
                The list of all nodes in the environment.
            K : float
                the percentage of the selection.
            debug_mode : bool, optional
                Indicates if the debug mode is enabled or not.

        """
        super().__init__(nodes, debug_mode)
        self.K = K
        self.debug_mode = debug_mode

    def random_client_selection(self) -> list:
        """
        Return the list of selected nodes randomlu.

        Parameters
        ----------


        Returns
        -------
            selected_clients (list): the list of the nodes.

        Examples
        --------
        >>> randomClientSelection.random_client_selection()
        """
        print(f"{Fore.LIGHTYELLOW_EX}[*] Starting Random client selection".format(Fore.LIGHTYELLOW_EX))
        selected_clients = []
        percentage = round(len(self.nodes) * self.K)
        for _ in range(0, percentage):
            client = random.choices(self.nodes)[0]
            if self.debug_mode:
                print(f"[*] The client {Fore.YELLOW}{client.get_name()}{Style.RESET_ALL} with id : "
                      f"{Fore.MAGENTA}{client.get_id()},{Style.RESET_ALL} has been selected")
            selected_clients.append(client)

        return selected_clients
