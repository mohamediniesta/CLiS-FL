from node.Node import Node


class CPUModel(object):
    def __init__(self, node: Node):
        self.node = node

    def get_node(self) -> Node:
        return self.node()

    def set_node(self, node: Node):
        self.node = node

    def check_cpu(self) -> bool:
        cpu_percentage = self.node.get_cpu_usage()

        if cpu_percentage >= 85:
            self.node.set_status(0)
            return False
        else:
            return True

    def update_cpu(self, cpu_usage):
        if self.node.cpu_usage + cpu_usage >= 99:
            self.node.set_status(0)
        else:
            self.node.set_cpu_usage(self.node.get_cpu_usage() + cpu_usage)
