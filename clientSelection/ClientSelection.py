
class ClientSelection(object):
    def __init__(self, nodes: list, debug_mode: bool = False):
        self.nodes = nodes
        self.debug_mode = debug_mode

    def getNodes(self) -> list:
        return self.nodes

    def getDebugMode(self) -> bool:
        return self.debug_mode
