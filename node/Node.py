import uuid


def generate_node_id() -> str:
    node_id: str = uuid.uuid4().hex
    return node_id


class Node(object):
    def __init__(self, name: str, data: str, mobility_mode: bool = False):
        self.node_id: list = generate_node_id()
        if not mobility_mode:
            self.mobility: int = None
        else:
            self.mobility: int = 5
        self.data: str = data
        self.name: str = name
        self.cpu_usage = 0
        self.memory_usage = 0
        self.battery_usage = 0

    def get_id(self):
        return self.node_id

    def get_name(self):
        return self.name
