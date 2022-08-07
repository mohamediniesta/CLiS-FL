import numpy as np
from tensorflow import keras
from models.Keras.model import create_model
from consumptionModel.StorageModel.StorageModel import StorageModel
from utils.generation import generateNodes


def sampling_data_to_clients(data, selected_client: list):
    num_clients = len(selected_client)
    num_items = int(data.shape[0] / num_clients)
    dict_users, all_idxs = {}, [i for i in range(len(data))]
    print(dict_users)
    print(all_idxs)
    for CLIENT in selected_client:
        storage_model = StorageModel(node=CLIENT)
        client_data = set(np.random.choice(all_idxs, num_items, replace=False))
        CLIENT.set_data(data=client_data, data_type="mnist")
        storage_model.add_to_storage(number_of_mega_bytes=5 * num_items)  # 5 Mega bytes per image (num_items)
        all_idxs = list(set(all_idxs) - CLIENT.getData())


# ! From here ---------------------------------------------------------------------------------------------------------

clients = generateNodes(number_of_nodes=200)

num_classes = 10

# Load the data and split it between train and test sets
train_dataset, test_dataset = keras.datasets.mnist.load_data()

print(train_dataset[0])
exit(0)

x_train, y_train = train_dataset
x_test, y_test = test_dataset

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255

x_test = x_test.astype("float32") / 255
# Make sure images have shape (28, 28, 1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")


exit(0)

sampling_data_to_clients(data=x_train, selected_client=clients)

print(clients[2].getData())

exit(0)



# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# ! until here ---------------------------------------------------------------------------------------------------------

model = create_model()

model.summary()

batch_size = 128
epochs = 2

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

score = model.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])
