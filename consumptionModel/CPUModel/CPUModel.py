from node.Node import Node


class CPUModel(object):
    """
     A class that represents the module of the processor consumption model of the nodes.

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
     check_cpu():
         Check if the node has reached the maximum CPU consumption level.
     update_cpu():
         Update the CPU consumption percentage of the node.
     """
    def __init__(self, node: Node):
        """
        Constructs all the necessary attributes for the CPUModel object.

        Parameters
        ----------
            node : Node
                The node assigned to this model.

        Examples
        --------
        >>> cpuModel = CPUModel(node=node1)

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
        >>> cpuModel.get_node()
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
        >>> cpuModel.set_node(node1)
        """
        self.node = node

    def check_cpu(self) -> bool:
        """
        Check if the node has reached the maximum CPU consumption level.

        Parameters
        ----------

        Returns
        -------
            status (bool): If the maximum level of consumption is reached or not.

        Examples
        --------
        >>> cpuModel.check_cpu()
        """
        cpu_percentage = self.node.get_cpu_usage()

        if cpu_percentage >= 85:
            self.node.set_status(0)
            return False
        else:
            return True

    def update_cpu(self, cpu_usage):
        """
        Update the CPU consumption percentage of the node.

        Parameters
        ----------
        cpu_usage: float
            the new level of processor consumption.

        Examples
        --------
        >>> cpuModel.update_cpu(65)
        """
        if self.node.cpu_usage + cpu_usage >= 99:
            self.node.set_status(0)
        else:
            self.node.set_cpu_usage(self.node.get_cpu_usage() + cpu_usage)
