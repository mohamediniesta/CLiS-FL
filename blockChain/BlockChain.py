import time
# from blockChain.utils import proof_of_work, is_valid_proof
from blockChain.Block.Block import Block


def proof_of_work(block):
    block.nonce = 0

    computed_hash = block.compute_hash()
    while not computed_hash.startswith('0' * Blockchain.difficulty):
        block.nonce += 1
        computed_hash = block.compute_hash()

    return computed_hash


def is_valid_proof(block, block_hash):
    return (block_hash.startswith('0' * Blockchain.difficulty) and
            block_hash == block.compute_hash())


class Blockchain:
    # ? difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_models = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def add_new_transaction(self, model):
        self.unconfirmed_models.append(model)

    def mine(self):
        if not self.unconfirmed_models:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_models,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_models = []
        return new_block.index
