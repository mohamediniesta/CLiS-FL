import numpy as np
import pandas as pd

n_clients = 100
n_samples = 500

cpu_power_range = (500, 4000)
memory_range = (200, 8000)
energy_range = (500, 15000)
dataset_size_range = (100, 10000)

data = []

for i in range(n_clients):
    cpu_power = np.random.randint(cpu_power_range[0], cpu_power_range[1], n_samples)
    memory = np.random.randint(memory_range[0], memory_range[1], n_samples)
    energy = np.random.randint(energy_range[0], energy_range[1], n_samples)
    dataset_size = np.random.randint(dataset_size_range[0], dataset_size_range[1], n_samples)
    device_info = np.random.choice(['Android', 'iOS', 'Windows', 'Mac'], n_samples)
    label = np.random.normal(0, 1, n_samples)

    client_data = pd.DataFrame({
        'CPU Power': cpu_power,
        'Memory': memory,
        'Energy': energy,
        'Dataset Size': dataset_size,
        'Label': label
    })

    data.append(client_data)
