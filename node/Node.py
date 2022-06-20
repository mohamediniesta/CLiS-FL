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
        self.cpu_usage: int = 0
        self.memory_usage: int = 0
        self.battery_usage: int = 0

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
