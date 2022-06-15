from node import Node


class PowNode(Node):
    def __init__(self, name: str, data: str):
        super().__init__(name, data)
        self.energy = 4000000
        self.cpu_power = 50
        self.memory = 4092

    def get_energy(self):
        return self.energy

    def get_cpu_power(self):
        return self.cpu_power

    def get_memory(self):
        return self.memory
