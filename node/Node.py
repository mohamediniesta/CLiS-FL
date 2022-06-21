import uuid


def generate_node_id() -> str:
    node_id: str = uuid.uuid4().hex
    return node_id


class Node(object):
    def __init__(self, name: str, data: str, data_type: str, mobility_mode: bool = False):
        self.node_id: str = generate_node_id()
        if not mobility_mode:
            self.mobility: int = None
        else:
            self.mobility: int = 5
        self.data: str = data
        self.data_type: str = data_type
        self.name: str = name
        self.cpu_usage: int = None
        self.memory_usage: int = None
        self.battery_usage: int = None
        self.total_energy: float = None
        self.energy_consumption: float = None
        self.current_energy: float = None
        self.cpu_power: float = None
        self.memory: int = None
        self.storage: int = None

    def get_total_energy(self):
        return self.total_energy

    def set_total_energy(self, total_energy):
        self.total_energy = total_energy

    def get_energy_consumption(self):
        return self.energy_consumption

    def set_energy_consumption(self, energy_consumption):
        self.energy_consumption = energy_consumption

    def get_current_energy(self):
        return self.current_energy

    def set_current_energy(self, current_energy):
        self.current_energy = current_energy

    def get_cpu_power(self):
        return self.cpu_power

    def get_memory(self):
        return self.memory

    def get_storage(self):
        return self.storage

    def get_id(self) -> str:
        return self.node_id

    def get_name(self) -> str:
        return self.name

    def get_data(self) -> list:
        return self.data

    def get_data_type(self) -> str:
        return self.data_type

    def set_data(self, data: str, data_type: str):
        self.data: list = data
        self.data_type: str = data_type
