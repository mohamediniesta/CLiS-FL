from node import Node
import random


class MidNode(Node):
    def __init__(self, name: str, mobility_mode: bool = False):
        super().__init__(name, mobility_mode)
        super().setTotalEnergy(2000)  # [mAh]
        current_energy = random.uniform(1000, 2000)
        super().setCurrentEnergy(current_energy)
        energy_consumption = random.uniform(25, 37)
        super().setEnergyConsumption(energy_consumption)

        super().setTotalStorage(15000)  # [Mega byte]
        super().setCurrentStorage(random.uniform(7000, 15000))
