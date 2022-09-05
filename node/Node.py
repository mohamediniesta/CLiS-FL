import uuid
import random
from datetime import datetime
import pandas as pd


def generateNode_id() -> str:
    """
    Generate a unique and random identifier for a new node.

    Returns
    -------
        node_id (str): The node identifier, represented by a hash.

    Examples
    --------
    >>> node.generateNode_id()
    """
    node_id: str = uuid.uuid4().hex
    return node_id


class Node(object):
    """
     A class that represents the basis of the node's module.

     ...

     Attributes
     ----------
     name : str
         The name of the node to be identified with.
     data : str
         The data available in the node.
     data_type : str
         The type of the data in the node.
     mobility_mode : bool
        Indicates if the node is mobile or not.
     node_id : str
        The node identifier, represented by a hash.
     ip_addr : str
        The IP address of the node in the network.
     status : int
        Indicates the status of the node if it is available and can be contacted. (1 = Yes, 0 = No)
     leader : bool
        Indicates whether the node is the leader of its network or not.
     gathered_data : any
        Data collected from other nodes or the server.
     battery_usage: int
        The percentage of the node's battery usage.
     total_energy: float
        The total energy capacity of the node.
     energy_consumption: float
        Indicates how much energy this node consumes in an operation.
     current_energy: float
        The current energy capacity in mAh.
     total_storage: int
        The total storage capacity of the node.
     current_storage: int
        The current storage capacity of the node.
     cpu_power: float
        The total power of the processor.
     cpu_usage: int
        The percentage of CPU usage.
     memory: int
        The memory capacity of the node.
     memory_usage: int
        The memory usage percentage of the node.

     Methods
     -------
     get_resources_information():
         Take all the information about the resources of this node.

     Notes
     -----
     The other methods are a group of getters and setters, so they are not explained for this module.

     """
    def __init__(self, name: str, data: str = None, data_type: str = None, mobility_mode: bool = False):
        """
        Constructs all the necessary attributes for the node object.

        Parameters
        ----------
            name : str
                The name of the node to be identified with.
            data : str, optional
                The data available in the node.
            data_type : str, optional
                The type of the data in the node.
            mobility_mode : bool, optional
                Indicates if the node is mobile or not.

        Examples
        --------
        >>> node = Node(name='node1')

        """
        self.ip_addr = None
        self.node_id: str = generateNode_id()
        if not mobility_mode:
            self.mobility: int = None
        else:
            self.mobility: int = 5
        self.data: str = data
        self.data_type: str = data_type
        self.name: str = name
        self.status: int = 1
        #  ? Energy Model.
        self.battery_usage: int = None
        self.total_energy: float = None
        self.energy_consumption: float = None
        self.current_energy: float = None
        #  ? Storage Model.
        self.total_storage: int = None
        self.current_storage: int = None
        # ? CPU Model.
        self.cpu_power: float = None
        self.cpu_usage: int = random.randint(30, 100)
        # ? Memory Model.
        self.memory: int = None
        self.memory_usage: int = random.randint(15, 100)
        # ? For Leader election.
        self.leader = False
        # ? The data gathered from other nodes.
        self.gathered_data = None

    def get_status(self):
        return self.status

    def set_status(self, status: int):
        self.status = status

    def get_total_energy(self) -> float:
        return self.total_energy

    def set_total_energy(self, total_energy: float):
        self.total_energy = total_energy

    def get_energy_consumption(self) -> float:
        return self.energy_consumption

    def set_energy_consumption(self, energy_consumption: float):
        self.energy_consumption = energy_consumption

    def get_current_energy(self) -> float:
        return self.current_energy

    def set_current_energy(self, current_energy: float):
        self.current_energy = current_energy

    def get_cpu_power(self) -> float:
        return self.cpu_power

    def get_memory(self) -> int:
        return self.memory

    def get_memory_usage(self) -> int:
        return self.memory_usage

    def set_memory_usage(self, memory_usage):
        self.memory_usage = memory_usage

    def get_cpu_usage(self) -> int:
        return self.cpu_usage

    def set_cpu_usage(self, cpu_usage):
        self.cpu_usage = cpu_usage

    def get_total_storage(self) -> int:
        return self.total_storage

    def set_total_storage(self, total_storage: int):
        self.total_storage = total_storage

    def get_current_storage(self) -> int:
        return self.current_storage

    def set_current_storage(self, current_storage: int):
        self.current_storage = current_storage

    def get_id(self) -> str:
        return self.node_id

    def get_name(self) -> str:
        return self.name

    def get_data_type(self) -> str:
        return self.data_type

    def get_data(self) -> list:
        return self.data

    def set_data(self, data: str, data_type: str):
        self.data: list = data
        self.data_type: str = data_type

    def get_ip_addr(self):
        return self.ip_addr

    def set_ip_addr(self, ip_addr):
        self.ip_addr = ip_addr

    def get_leader(self):
        return self.leader

    def set_leader(self, leader: bool):
        self.leader = leader

    def get_gathered_data(self) -> pd.DataFrame:
        return self.gathered_data

    def set_gathered_data(self, gathered_data: pd.DataFrame):
        self.gathered_data = gathered_data

    def get_resources_information(self):
        """
        Take all the information about the resources of this node.

        Returns
        -------
           information (tuple): All resource information represented by a tuple of 13 information.

        Examples
        --------
        >>> node.get_resources_information()
        """
        # ? Structure : CPUPower, CPU Usage,Memory,MemoryUsage,TotalStorage,CurrentStorage,BatteryUsage, TotalEnergy,
        # ? EnergyConsumption, CurrentEnergy, DataLength, Time
        return self.name, self.cpu_power, self.cpu_usage, self.memory, self.memory_usage, \
               self.total_storage, self.current_storage, self.battery_usage, self.total_energy, \
               self.energy_consumption, self.current_energy, len(self.data), datetime.now()
