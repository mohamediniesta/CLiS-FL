from node.Node import Node
from constants.resource_constants import MIN_BATTERY


class EnergyModel(object):
    """
     A class that represents the module of the energy consumption model of the nodes.

     ...

     Attributes
     ----------
     node : Node
         The node assigned to this model.

     Methods
     -------
     get_node(): Node
         Return the node.
     set_node():
         Assign this consumption model to a node.
     consume_energy():
         Consume a certain level of energy from the node according to its category.
     check_battery():
         Update the CPU consumption percentage of the node.
     """

    def __init__(self, node: Node):
        """
        Constructs all the necessary attributes for the EnergyModel object.

        Parameters
        ----------
            node : Node
                The node assigned to this model.

        Examples
        --------
        >>> energyModel = EnergyModel(node=node1)

        """
        self.node = node

    def get_node(self) -> Node:
        """
        Return the instance of the node.

        Parameters
        ----------


        Returns
        -------
            nodes (Node): The node's instance.

        Examples
        --------
        >>> energyModel.get_node()
        """
        return self.node()

    def set_node(self, node: Node):
        """
        Assign this consumption model to a node.

        Parameters
        ----------
        node: Node
            the node's instance.

        Examples
        --------
        >>> energyModel.set_node(node1)
        """
        self.node = node

    def consume_energy(self) -> float:
        """
        Consume a certain level of energy from the node according to its category.

        Parameters
        ----------

        Returns
        -------
            new_energy (float): The new energy level of the node.

        Examples
        --------
        >>> energyModel.consume_energy()
        """
        node_energy_consumption = self.node.get_energy_consumption()
        node_current_energy = self.node.get_current_energy()
        new_energy = node_current_energy - node_energy_consumption
        return new_energy

    def check_battery(self):
        """
        Check that the node 's battery is not depleted.

        Parameters
        ----------

        Examples
        --------
        >>> cpuModel.check_battery()
        """
        if ((self.node.get_current_energy() / self.node.get_total_energy()) * 100) <= MIN_BATTERY:
            self.node.set_status(0)
