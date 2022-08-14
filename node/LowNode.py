from node import Node
import random


class LowNode(Node):
    def __init__(self, name: str, mobility_mode: bool = False):
        super().__init__(name, mobility_mode)
        super().setTotalEnergy(600)
        current_energy = random.uniform(400, 600)
        super().setCurrentEnergy(current_energy)
        energy_consumption = random.uniform(11, 15)
        super().setEnergyConsumption(energy_consumption)

        super().setTotalStorage(2000)  # [Mega byte]
        super().setCurrentStorage(random.uniform(1000, 2000))
