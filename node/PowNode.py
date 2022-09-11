# pylint: disable = C0114, C0115, C0116, C0103

import random
from node import Node


class PowNode(Node):
    """
     A class that represents the module of a powerful node.

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
        Constructs all the necessary attributes for the PowNode object.

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
        self.battery_mode = random.randint(0, 1)  # ? Battery (1) or in charge (0).
        if self.battery_mode == 1:
            super().set_total_energy(6000)  # ? [mAh]
            # ? current battery capacity, from 2500 to 6000 [mAh]
            current_energy = random.randint(2500, 6000)
            super().set_current_energy(current_energy)  # ? [mAh]
            energy_consumption = random.uniform(25, 50)
            super().set_energy_consumption(energy_consumption)

        super().set_total_storage(50000)  # ? [Mega byte]
        super().set_current_storage(random.uniform(25000, 50000))
