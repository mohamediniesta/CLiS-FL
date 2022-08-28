from hashlib import sha256
import json


class Block:
    def __init__(self, index, model, timestamp, previous_hash, nonce=0):
        self.index = index
        self.model = model
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
