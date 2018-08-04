from block import Block
from blockchain import Blockchain

if __name__ == '__main__':
    blockchain = Blockchain()
    block_a = Block('information a')
    block_b = Block('information b')
    blockchain.add_block(block_a)
    blockchain.add_block(block_b)
    # Remember: blockchain.blockchain is our list
    # of blocks
    print(blockchain.blockchain)

    print(blockchain.is_valid()) # Should return True.
    # Tampers with the ORDER of the blocks.
    blockchain.blockchain = blockchain.blockchain[::-1]
    print(blockchain.blockchain) # Oh no, the blockchain list is now reversed!
    print(blockchain.is_valid()) # However this still returns True...
