from node import Node
import random


class PowNode(Node):
    def __init__(self, name: str, data: str, mobility_mode: bool = False):
        super().__init__(name, data, mobility_mode)
        self.battery_mode = random.randint(0, 1)  # Battery (1) or in charge (0).
        if self.battery_mode == 1:
            super().set_total_energy(6000)  # [mAh]
            current_energy = random.randint(2500, 6000)  # current battery capacity, from 2500 to 6000 [mAh]
            super().set_current_energy(current_energy)  # [mAh]
            energy_consumption = random.uniform(25, 50)
            super().set_energy_consumption(energy_consumption)

        super().set_total_storage(50000)  # [Mega byte]
        super().set_current_storage(random.uniform(25000, 50000))
