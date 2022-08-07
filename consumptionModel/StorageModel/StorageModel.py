from node.Node import Node


class StorageModel(object):
    def __init__(self, node: Node):
        self.node = node

    def getNode(self) -> Node:
        return self.node()

    def setNode(self, node: Node):
        self.node = node

    def addToStorage(self, number_of_mega_bytes: float) -> float:
        if number_of_mega_bytes > self.node.current_storage:
            # print("Insufficient space! in {0}".format(self.node.getName()))
            self.node.setStatus(0)
        else:
            self.node.setCurrentStorage(self.node.getCurrentStorage() - number_of_mega_bytes)

    def checkStorage(self) -> bool:
        storage_p = (self.node.getCurrentStorage() / self.node.getTotalStorage()) * 100

        if storage_p <= 0:
            self.node.setStatus(0)
            return False
        else:
            return True
