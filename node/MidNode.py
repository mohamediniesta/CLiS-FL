import random
from node import Node


class MidNode(Node):
    """
     A class that represents the module of a medium power node.

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
        >>> node = PowNode(name='node1')
        """
        super().__init__(name, mobility_mode)
        super().set_total_energy(2000)  # ? [mAh]
        current_energy = random.uniform(1000, 2000)
        super().set_current_energy(current_energy)
        energy_consumption = random.uniform(25, 37)
        super().set_energy_consumption(energy_consumption)

        super().set_total_storage(15000)  # ? [Mega byte]
        super().set_current_storage(random.uniform(7000, 15000))
