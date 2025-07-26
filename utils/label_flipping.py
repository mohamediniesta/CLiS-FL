poisoning_percentage = 0.1
num_clients = len(emnist_train.client_ids)

def poison_dataset(dataset):
    return dataset.map(
        lambda x: {
            'pixels': x['pixels'],
            'label': (x['label'] + 1) % 10
        },
        num_parallel_calls=tf.data.AUTOTUNE
    )

poisoned_clients = np.random.choice(
    emnist_train.client_ids,
    size=int(num_clients * poisoning_percentage),
    replace=False
)

federated_train_data_poisoned = [
    poison_dataset(emnist_train.create_tf_dataset_for_client(client_id))
    if client_id in poisoned_clients
    else emnist_train.create_tf_dataset_for_client(client_id)
    for client_id in emnist_train.client_ids
]
