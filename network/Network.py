# pylint: disable = C0114, C0115, C0116, C0103

class Network:
    """
     A class that represents the module of a network of nodes.

     ...

     Attributes
     ----------
     nodes : list
         The list of all nodes in the environment.
     network_number : int
         The network number.
     debug_mode : bool
         Indicates if the debug mode is enabled or not.

     Methods
     -------
     assign_ip_addresses():
         Give an ip address to all nodes assigned to this network.
     get_network_number():
         Return the number of the network.
     get_nodes():
         Return the list of all nodes.
     get_network_leader():
         Return the leader of the network.
     set_network_leader():
         Assign a leader to the network.
     """
    def __init__(self, nodes: list, network_number: int, debug_mode: bool = False):
        """
        Constructs all the necessary attributes for the Network object.

        Parameters
        ----------
            nodes : list
                The list of all nodes in the environment.
            network_number : int
                The network number.
            debug_mode : bool, optional
                Indicates if the debug mode is enabled or not.

        """
        self.nodes = nodes
        self.network_number = network_number
        self.debug_mode = debug_mode
        self.prefix_ip = f"192.168.{network_number}."
        self.network_leader = None

    def assign_ip_addresses(self):
        """
        Assign an ip address to all nodes on the network.

        Examples
        --------
        >>> network.assign_ip_addresses()
        """
        index = 2
        for node in self.nodes:
            ip_addr = self.prefix_ip + str(index)
            node.set_ip_addr(ip_addr)
            index += 1

    def get_network_number(self):
        """
        Return the number of the network.

        Parameters
        ----------


        Returns
        -------
            network_number (int): The network number.

        Examples
        --------
        >>> network.get_network_number()
        """
        return self.network_number

    def get_nodes(self) -> list:
        """
        Return the list of the nodes.

        Parameters
        ----------


        Returns
        -------
            nodes (list): the list of the nodes.

        Examples
        --------
        >>> network.get_nodes()
        """
        return self.nodes

    def get_network_leader(self):
        """
        Return the leader of the network.

        Parameters
        ----------


        Returns
        -------
            network_leader (Node): the instance of the leader node of the network.

        Examples
        --------
        >>> network.get_network_leader()
        """
        return self.network_leader

    def set_network_leader(self, network_leader):
        """
        Assign a leader to the network.

        Parameters
        ----------
            network_leader : Node
                The new node leader for the network.

        Returns
        -------
            network_leader (Node): the instance of the leader node of the network.

        Examples
        --------
        >>> network.set_network_leader(node1)
        """
        self.network_leader = network_leader
