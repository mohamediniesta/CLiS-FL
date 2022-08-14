from node.Node import Node
from constants.resource_constants import MIN_BATTERY


class EnergyModel(object):
    def __init__(self, node: Node):
        self.node = node

    def get_node(self) -> Node:
        return self.node()

    def set_node(self, node: Node):
        self.node = node

    def consume_energy(self) -> float:
        node_energy_consumption = self.node.get_energy_consumption()
        node_current_energy = self.node.get_current_energy()
        new_energy = node_current_energy - node_energy_consumption
        return new_energy

    def check_battery(self):
        if ((self.node.get_current_energy() / self.node.get_total_energy()) * 100) <= MIN_BATTERY:
            self.node.set_status(0)
