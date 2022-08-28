from blockChain.BlockChain import Blockchain

blockChain = Blockchain()

blockChain.create_genesis_block()

print(blockChain.last_block.hash)
