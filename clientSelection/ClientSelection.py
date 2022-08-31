
class ClientSelection(object):
    """
     A class that represents the basis of the client selection module.

     ...

     Attributes
     ----------
     nodes : list
         The list of all nodes in the environment.
     debug_mode : bool
         Indicates if the debug mode is enabled or not.

     Methods
     -------
     get_nodes():
         Return the list of all nodes.
     get_debug_mode():
         Return if the debug_mode is enabled.
     """
    def __init__(self, nodes: list, debug_mode: bool = False):
        """
        Constructs all the necessary attributes for the ClientSelection object.

        Parameters
        ----------
            nodes : list
                The list of all nodes in the environment.
            debug_mode : bool, optional
                Indicates if the debug mode is enabled or not.

        """
        self.nodes = nodes
        self.debug_mode = debug_mode

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
        >>> clientSelection.get_nodes()
        """
        return self.nodes

    def get_debug_mode(self) -> bool:
        """
        Return if the debug_mode is enabled.

        Returns
        -------
            debug_mode (bool): Indicates if the debug mode is enabled or not.

        Examples
        --------
        >>> clientSelection.get_debug_mode()
        """
        return self.debug_mode
