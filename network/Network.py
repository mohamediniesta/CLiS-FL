class Network(object):
    def __init__(self, nodes: list, network_number: int, debug_mode: bool = False):
        self.nodes = nodes
        self.network_number = network_number
        self.debug_mode = debug_mode
        self.prefix_ip = "192.168.{0}.".format(network_number)
        self.network_leader = None

    def assign_ip_addresses(self):
        index = 2
        for node in self.nodes:
            ip_addr = self.prefix_ip + str(index)
            node.set_ip_addr(ip_addr)
            index += 1

    def get_network_number(self):
        return self.network_number

    def get_nodes(self) -> list:
        return self.nodes

    def get_network_leader(self):
        return self.network_leader

    def set_network_leader(self, network_leader):
        self.network_leader = network_leader
