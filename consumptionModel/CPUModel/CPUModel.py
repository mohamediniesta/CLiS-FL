from node.Node import Node


class CPUModel(object):
    def __init__(self, node: Node):
        self.node = node

    def getNode(self) -> Node:
        return self.node()

    def setNode(self, node: Node):
        self.node = node

    def checkCpu(self) -> bool:
        cpu_percentage = self.node.getCpuUsage()

        if cpu_percentage >= 85:
            self.node.setStatus(0)
            return False
        else:
            return True

    def updateCpu(self, cpu_usage):
        if self.node.cpu_usage + cpu_usage >= 99:
            self.node.setStatus(0)
        else:
            self.node.setCpuUsage(self.node.getCpuUsage() + cpu_usage)
