import uuid


def generate_node_id() -> str:

    node_id = uuid.uuid4().hex
    return node_id


class Node(object):
    def __init__(self, name: str, data: str):
        self.node_id = generate_node_id()
        self.data = data
        self.name = name

    def get_id(self):
        return self.node_id

    def get_name(self):
        return self.name
