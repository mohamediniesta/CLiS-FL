from node import Node
import random


class LowNode(Node):
    def __init__(self, name: str, data: str, mobility_mode: bool = False):
        super().__init__(name, data, mobility_mode)
        super().set_total_energy(600)
        current_energy = random.uniform(400, 600)
        super().set_current_energy(current_energy)
        energy_consumption = random.uniform(11, 15)
        super().set_energy_consumption(energy_consumption)

        super().set_total_storage(2000)  # [Mega byte]
        super().set_current_storage(random.uniform(1000, 2000))
