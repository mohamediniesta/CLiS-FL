from node.Node import Node


class EnergyModel(object):
    def __init__(self, node: Node):
        self.node = node

    def getNode(self) -> Node:
        return self.node()

    def setNode(self, node: Node):
        self.node = node

    def consumeEnergy(self) -> float:
        node_energy_consumption = self.node.getEnergyConsumption()
        node_current_energy = self.node.getCurrentEnergy()
        new_energy = node_current_energy - node_energy_consumption
        return new_energy

    def checkBattery(self) -> bool:
        battery_p = (self.node.getCurrentEnergy() /
                     self.node.getTotalEnergy()) * 100

        if battery_p <= 5:
            self.node.setStatus(0)
            return False
        else:
            return True
