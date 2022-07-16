import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from constants.federated_learning import LOCAL_EP
from constants.model_constants import LR, MOMENTUM, LOCAL_BS
from consumptionModel.EnergyModel.EnergyModel import EnergyModel
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


def train_val_test(dataset, idxs):
    """
    Returns train, validation and test dataLoaders for a given dataset
    and user indexes.
    """
    # ? Split indexes for train, validation, and test (80, 10, 10)
    idxs_train = idxs[:int(0.8 * len(idxs))]
    idxs_val = idxs[int(0.8 * len(idxs)):int(0.9 * len(idxs))]
    idxs_test = idxs[int(0.9 * len(idxs)):]
    trainLoader = DataLoader(DatasetSplit(dataset, idxs_train), batch_size=LOCAL_BS, shuffle=True)
    validLoader = DataLoader(DatasetSplit(dataset, idxs_val), batch_size=int(len(idxs_val) / 10), shuffle=False)
    testLoader = DataLoader(DatasetSplit(dataset, idxs_test), batch_size=int(len(idxs_test) / 10), shuffle=False)
    return trainLoader, validLoader, testLoader


class ClientUpdate(object):
    def __init__(self, dataset, idxs, node):
        self.trainLoader, self.validLoader, self.testLoader = train_val_test(dataset, list(idxs))
        self.device = 'cpu'
        # ? Default criterion set to NLL loss function
        self.node = node
        self.criterion = nn.NLLLoss().to(self.device)
        self.energy_model = EnergyModel(node=self.node)
        self.storage_model = StorageModel(node=self.node)

    def update_weights(self, model, global_round):
        # ? Set mode to train model
        energy = 0
        model.train()
        epoch_loss = []

        # ? Set optimizer for the local updates
        optimizer = torch.optim.SGD(model.parameters(), lr=LR, momentum=MOMENTUM)
        for iteration in range(LOCAL_EP):

            if self.node.get_total_energy() is not None:
                # ? Battery consumption.
                new_energy = self.energy_model.consume_energy()
                self.node.set_current_energy(new_energy)
                energy = energy + self.node.get_energy_consumption()

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
        self.storage_model.add_to_storage(number_of_mega_bytes=100)

        return model.state_dict(), sum(epoch_loss) / len(epoch_loss), energy

    def inference(self, model):
        """ Returns the inference accuracy and loss.
        """

        model.eval()
        loss, total, correct = 0.0, 0.0, 0.0

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
