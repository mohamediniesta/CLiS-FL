from node.Node import Node


class StorageModel(object):
    def __init__(self, node: Node):
        self.node = node

    def get_node(self) -> Node:
        return self.node()

    def set_node(self, node: Node):
        self.node = node

    def add_to_storage(self, number_of_mega_bytes: float) -> float:
        self.node.set_current_storage(self.node.get_current_storage() - number_of_mega_bytes)

    def check_storage(self) -> bool:
        storage_p = (self.node.get_current_storage() / self.node.get_total_storage()) * 100

        if storage_p <= 0:
            return False
        else:
            return True
