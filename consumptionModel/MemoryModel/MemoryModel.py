from node.Node import Node


class MemoryModel(object):
    def __init__(self, node: Node):
        self.node = node

    def getNode(self) -> Node:
        return self.node()

    def setNode(self, node: Node):
        self.node = node

    def checkMemory(self) -> bool:
        memory_percentage = self.node.getMemoryUsage()

        if memory_percentage >= 90:
            self.node.setStatus(0)
            return False
        else:
            return True

    def updateMemory(self, memory_usage):
        if self.node.memory_usage + memory_usage >= 99:
            self.node.setStatus(0)
        else:
            self.node.setMemoryUsage(self.node.getMemoryUsage() + memory_usage)
