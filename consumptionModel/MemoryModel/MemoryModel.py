from node.Node import Node


class MemoryModel(object):
    def __init__(self, node: Node):
        self.node = node

    def get_node(self) -> Node:
        return self.node()

    def set_node(self, node: Node):
        self.node = node

    def check_memory(self) -> bool:
        memory_percentage = self.node.get_memory_usage()

        if memory_percentage >= 90:
            self.node.set_status(0)
            return False
        else:
            return True

    def update_memory(self, memory_usage):
        if self.node.memory_usage + memory_usage >= 99:
            self.node.set_status(0)
        else:
            self.node.set_memory_usage(self.node.get_memory_usage() + memory_usage)
