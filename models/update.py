import torch
import random
from torch import nn
from torch.utils.data import DataLoader, Dataset
from constants.federated_learning import LOCAL_EP
from consumptionModel.CPUModel.CPUModel import CPUModel
from constants.model_constants import LR, MOMENTUM, LOCAL_BS
from consumptionModel.EnergyModel.EnergyModel import EnergyModel
from consumptionModel.MemoryModel.MemoryModel import MemoryModel
from consumptionModel.StorageModel.StorageModel import StorageModel


class DatasetSplit(Dataset):
    """An abstract Dataset class wrapped around Pytorch Dataset class.
    """

    def __init__(self, dataset, idxs):
        self.dataset = dataset
        self.idxs = [int(i) for i in idxs]

    def __len__(self):
        return len(self.idxs)

    def __getitem__(self, item):
        image, label = self.dataset[self.idxs[item]]
        return image.clone().detach(), torch.tensor(label)


def trainValTest(dataset, idxs):
    # ? Split indexes for train, validation, and test (80, 10, 10)
    idxs_train, idxs_val, idxs_test = \
        idxs[:int(0.8 * len(idxs))], \
        idxs[int(0.8 * len(idxs)):int(0.9 * len(idxs))], \
        idxs[int(0.9 * len(idxs)):]

    trainLoader, validLoader, testLoader = \
        DataLoader(DatasetSplit(dataset, idxs_train), batch_size=LOCAL_BS, shuffle=True), \
        DataLoader(DatasetSplit(dataset, idxs_val), batch_size=32, shuffle=False), \
        DataLoader(DatasetSplit(dataset, idxs_test), batch_size=32, shuffle=False)

    return trainLoader, validLoader, testLoader


class ClientUpdate(object):
    def __init__(self, dataset, idxs, node):
        self.node = node
        # ? Init our resources consumption Models.
        self.energy_model = EnergyModel(node=self.node)
        self.storage_model = StorageModel(node=self.node)
        self.memory_model = MemoryModel(node=self.node)
        self.cpu_model = CPUModel(node=self.node)

        # ? Split the data.
        self.trainLoader, self.validLoader, self.testLoader = trainValTest(dataset, list(idxs))

        # ? Increase CPU and memory usage randomly.
        self.memory_model.updateMemory(random.randint(3, 5))
        self.cpu_model.updateCpu(random.randint(3, 5))

        # ? Using CPU as device and not GPU.
        self.device = 'cpu'
        # ? Default criterion set to NLL loss function
        self.criterion = nn.NLLLoss().to(self.device)

    def updateWeights(self, model, global_round):
        if self.node.getStatus() == 0:
            return
        # ? Set mode to train model
        energy = 0
        model.train()
        epoch_loss = []

        # ? Set optimizer for the local updates
        optimizer = torch.optim.SGD(model.parameters(), lr=LR, momentum=MOMENTUM)
        for iteration in range(LOCAL_EP):

            if self.node.getTotalEnergy() is not None:
                # ? Battery consumption.
                new_energy = self.energy_model.consumeEnergy()
                self.node.setCurrentEnergy(new_energy)
                energy = energy + self.node.getEnergyConsumption()

            batch_loss = []

            for batch_idx, (images, labels) in enumerate(self.trainLoader):
                images, labels = images.to(self.device), labels.to(self.device)

                model.zero_grad()
                log_probs = model(images)
                loss = self.criterion(log_probs, labels)
                loss.backward()
                optimizer.step()
                verbose = 0
                if verbose and (batch_idx % 10 == 0):
                    print('| Global Round : {} | Local Epoch : {} | [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                        global_round, iteration, batch_idx * len(images),
                        len(self.trainLoader.dataset), 100. * batch_idx / len(self.trainLoader), loss.item()))

                batch_loss.append(loss.item())

            epoch_loss.append(sum(batch_loss) / len(batch_loss))
        # ? Adding the model size to the storage of device.
        self.storage_model.addToStorage(number_of_mega_bytes=100)
        # ? Increase CPU and memory usage randomly.
        self.memory_model.updateMemory(random.randint(30, 60))
        self.cpu_model.updateCpu(random.randint(30, 60))

        if self.node.getStatus() == 0:
            return 

        return model.state_dict(), sum(epoch_loss) / len(epoch_loss), energy

    def inference(self, model):
        """ Returns the inference accuracy and loss.
        """

        model.eval()
        loss, total, correct = 0.0, 0.0, 0.0

        if self.node.getTotalEnergy() is not None:
            # ? Battery consumption.
            new_energy = self.energy_model.consumeEnergy()
            self.node.setCurrentEnergy(new_energy)

        for batch_idx, (images, labels) in enumerate(self.testLoader):
            images, labels = images.to(self.device), labels.to(self.device)

            # ? Inference
            outputs = model(images)
            batch_loss = self.criterion(outputs, labels)
            loss += batch_loss.item()

            # ? Prediction
            _, predictions_labels = torch.max(outputs, 1)
            predictions_labels = predictions_labels.view(-1)
            correct += torch.sum(torch.eq(predictions_labels, labels)).item()
            total += len(labels)

        accuracy = correct / total
        return accuracy, loss
