from blockChain.BlockChain import Blockchain


def proof_of_work(block):
    block.nonce = 0

    computed_hash = block.compute_hash()
    while not computed_hash.startswith('0' * 2):
        block.nonce += 1
        computed_hash = block.compute_hash()

    return computed_hash


def is_valid_proof(block, block_hash):
    return (block_hash.startswith('0' * 2) and
            block_hash == block.compute_hash())
