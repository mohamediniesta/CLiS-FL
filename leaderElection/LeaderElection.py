# pylint: disable = C0114, C0115, C0116, C0103

from node.Node import Node


class LeaderElection(object):

    def __init__(self, nodes: list, debug_mode: bool = False):
        self.nodes = nodes
        self.debug_mode = debug_mode

    def min_find(self) -> Node:
        leader = self.nodes[0]
        for i in range(1, len(self.nodes)):
            leader_id = int(leader.get_id(), 16)
            if leader_id > int(self.nodes[i].get_id(), 16):
                leader = self.nodes[i]
        leader.set_leader(True)
        return leader
