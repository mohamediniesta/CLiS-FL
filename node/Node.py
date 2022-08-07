import uuid
import random
from datetime import datetime
import pandas as pd


def generateNode_id() -> str:
    node_id: str = uuid.uuid4().hex
    return node_id


class Node(object):
    def __init__(self, name: str, data: str, data_type: str, mobility_mode: bool = False):
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

    def getStatus(self):
        return self.status

    def setStatus(self, status: int):
        self.status = status

    def getTotalEnergy(self) -> float:
        return self.total_energy

    def setTotalEnergy(self, total_energy: float):
        self.total_energy = total_energy

    def getEnergyConsumption(self) -> float:
        return self.energy_consumption

    def setEnergyConsumption(self, energy_consumption: float):
        self.energy_consumption = energy_consumption

    def getCurrentEnergy(self) -> float:
        return self.current_energy

    def setCurrentEnergy(self, current_energy: float):
        self.current_energy = current_energy

    def getCpuPower(self) -> float:
        return self.cpu_power

    def getMemory(self) -> int:
        return self.memory

    def getMemoryUsage(self) -> int:
        return self.memory_usage

    def setMemoryUsage(self, memory_usage):
        self.memory_usage = memory_usage

    def getCpuUsage(self) -> int:
        return self.cpu_usage

    def setCpuUsage(self, cpu_usage):
        self.cpu_usage = cpu_usage

    def getTotalStorage(self) -> int:
        return self.total_storage

    def setTotalStorage(self, total_storage: int):
        self.total_storage = total_storage

    def getCurrentStorage(self) -> int:
        return self.current_storage

    def setCurrentStorage(self, current_storage: int):
        self.current_storage = current_storage

    def getId(self) -> str:
        return self.node_id

    def getName(self) -> str:
        return self.name

    def getDataType(self) -> str:
        return self.data_type

    def getData(self) -> list:
        return self.data

    def setData(self, data: str, data_type: str):
        self.data: list = data
        self.data_type: str = data_type

    def getIpAddr(self):
        return self.ip_addr

    def setIpAddr(self, ip_addr):
        self.ip_addr = ip_addr

    def getLeader(self):
        return self.leader

    def setLeader(self, leader: bool):
        self.leader = leader

    def getGatheredData(self) -> pd.DataFrame:
        return self.gathered_data

    def setGatheredData(self, gathered_data: pd.DataFrame):
        self.gathered_data = gathered_data

    def getResourcesInformation(self):
        # ? Structure : CPUPower, CPU Usage,Memory,MemoryUsage,TotalStorage,CurrentStorage,BatteryUsage, TotalEnergy,
        # ? EnergyConsumption, CurrentEnergy, DataLength, Time
        return self.name, self.cpu_power, self.cpu_usage, self.memory, self.memory_usage, \
               self.total_storage, self.current_storage, self.battery_usage, self.total_energy, \
               self.energy_consumption, self.current_energy, len(self.data), datetime.now()
