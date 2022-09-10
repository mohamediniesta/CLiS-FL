from node.Node import Node


class MemoryModel:
    """
     A class that represents the module of the memory consumption model of the nodes.

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
     check_memory():
         Check if the node has reached the maximum Memory consumption level.
     update_memory():
         Update the Memory consumption percentage of the node.
     """
    def __init__(self, node: Node):
        """
        Constructs all the necessary attributes for the MemoryModel object.

        Parameters
        ----------
            node : Node
                The node assigned to this model.

        Examples
        --------
        >>> memoryModel = MemoryModel(node=node1)

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
        >>> memoryModel.get_node()
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
        >>> memoryModel.set_node(node1)
        """
        self.node = node

    def check_memory(self) -> bool:
        """
        Check if the node has reached the maximum Memory consumption level.

        Parameters
        ----------

        Returns
        -------
            status (bool): If the maximum level of consumption is reached or not.

        Examples
        --------
        >>> memoryModel.check_memory()
        """
        memory_percentage = self.node.get_memory_usage()

        if memory_percentage >= 90:
            self.node.set_status(0)
            return False
        return True

    def update_memory(self, memory_usage):
        """
        Update the Memory consumption percentage of the node.

        Parameters
        ----------
        memory_usage: float
            the new level of processor consumption.

        Examples
        --------
        >>> memoryModel.update_cpu(57)
        """
        if self.node.memory_usage + memory_usage >= 99:
            self.node.set_status(0)
        else:
            self.node.set_memory_usage(self.node.get_memory_usage() + memory_usage)
