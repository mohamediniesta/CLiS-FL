from node.Node import Node


class StorageModel:
    """
     A class that represents the module of the storage consumption model of the nodes.

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
     check_storage():
         Check if the node has reached the maximum storage consumption level.
     add_to_storage():
         Add files to the node and thus fill the storage.
     """
    def __init__(self, node: Node):
        """
        Constructs all the necessary attributes for the StorageModel object.

        Parameters
        ----------
            node : Node
                The node assigned to this model.

        Examples
        --------
        >>> storageModel = StorageModel(node=node1)

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
        >>> storageModel.get_node()
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
        >>> storageModel.set_node(node1)
        """
        self.node = node

    def add_to_storage(self, number_of_mega_bytes: float) -> float:
        """
        Add files to the node and thus fill the storage.

        Parameters
        ----------
        number_of_mega_bytes: float
            The size of the files added to the storage.

        Examples
        --------
        >>> storageModel.add_to_storage(658)
        """
        if number_of_mega_bytes > self.node.current_storage:
            # print("Insufficient space! in {0}".format(self.node.getName()))
            self.node.set_status(0)
        else:
            self.node.set_current_storage(self.node.get_current_storage()
                                          - number_of_mega_bytes)

    def check_storage(self) -> bool:
        """
        Check if the node has reached the maximum Storage consumption level.

        Parameters
        ----------

        Returns
        -------
            status (bool): If the maximum level of consumption is reached or not.

        Examples
        --------
        >>> storageModel.check_storage()
        """
        storage_p = (self.node.get_current_storage() /
                     self.node.get_total_storage()) * 100

        if storage_p <= 0:
            self.node.set_status(0)
            return False
        else:
            return True
