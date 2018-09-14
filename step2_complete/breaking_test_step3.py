from block import Block
from blockchain import Blockchain

if __name__ == '__main__':
    blockchain = Blockchain()
    for i in range(10):
        block = Block(f'information {i}')
        blockchain.add_block(block)

    # Remember: blockchain.blockchain is our list
    # of blocks
    print([block.data for block in blockchain.blockchain])

    print(blockchain.is_valid()) # Should return True.
    # Changes data inside the blockchain and recalculates the whole
    blockchain.blockchain[5].data = 'Tampered information!!!'
    for i, block in enumerate(blockchain.blockchain[5:]):
        idx = blockchain.blockchain.index(block)
        # block.data = f'Tampered information {i}'
        block.hash = block.calculate_hash()
        if idx != len(blockchain.blockchain) - 1:
            blockchain.blockchain[idx + 1].previous_hash = block.hash

    print([block.data for block in blockchain.blockchain]) # Oh boy! We've tampered with the data of a block!
    print(blockchain.is_valid()) # And the validating function didn't detect this!
