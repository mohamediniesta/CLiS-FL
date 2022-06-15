
class ClientSelection(object):
    def __init__(self, nodes: list, debug_mode: bool = False):
        self.nodes = nodes
        self.debug_mode = debug_mode

    def get_nodes(self) -> list:
        return self.nodes

    def get_debug_mode(self) -> bool:
        return self.debug_mode
