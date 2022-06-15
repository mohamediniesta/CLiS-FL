import random
from node import PowNode, MidNode, LowNode


def generateNodes(number_of_nodes: int) -> list:
    nodes = []
    for i in range(0, number_of_nodes):
        rate = random.randint(0, 2)
        if rate == 0:
            node = LowNode(name="Node {}".format(i), data="test")
        elif rate == 1:
            node = MidNode(name="Node {}".format(i), data="test")
        else:
            node = PowNode(name="Node {}".format(i), data="test")
        nodes.append(node)
    return nodes
