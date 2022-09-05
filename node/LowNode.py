from node import Node
import random


class LowNode(Node):
    """
     A class that represents the module of a low power node.

     ...

     Attributes
     ----------
     name : str
        The node of the node to identify it.
     mobility_mode : bool, optional
        Indicates whether the node is mobile or stationary.

     """
    def __init__(self, name: str, mobility_mode: bool = False):
        """
        Constructs all the necessary attributes for the MidNode object.

        Parameters
        ----------
            name : str
                The node of the node to identify it.
            mobility_mode : bool, optional
                Indicates whether the node is mobile or stationary.

        Examples
        --------
        >>> node = LowNode(name='node1')
        """
        super().__init__(name, mobility_mode)
        super().set_total_energy(600)
        current_energy = random.uniform(400, 600)
        super().set_current_energy(current_energy)
        energy_consumption = random.uniform(11, 15)
        super().set_energy_consumption(energy_consumption)

        super().set_total_storage(2000)  # [Mega byte]
        super().set_current_storage(random.uniform(1000, 2000))
