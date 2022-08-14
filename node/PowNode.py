from node import Node
import random


class PowNode(Node):
    def __init__(self, name: str, mobility_mode: bool = False):
        super().__init__(name, mobility_mode)
        self.battery_mode = random.randint(0, 1)  # Battery (1) or in charge (0).
        if self.battery_mode == 1:
            super().setTotalEnergy(6000)  # [mAh]
            current_energy = random.randint(2500, 6000)  # current battery capacity, from 2500 to 6000 [mAh]
            super().setCurrentEnergy(current_energy)  # [mAh]
            energy_consumption = random.uniform(25, 50)
            super().setEnergyConsumption(energy_consumption)

        super().setTotalStorage(50000)  # [Mega byte]
        super().setCurrentStorage(random.uniform(25000, 50000))
