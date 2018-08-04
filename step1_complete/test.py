from block import Block
from blockchain import Blockchain

if __name__ == "__main__":
    blockchain = Blockchain()
    block = Block('random data here')
    print(blockchain.is_valid())
    blockchain.add_block(block)
    print(blockchain.is_valid())
    block.data = 'tampered data!!!'
    print(blockchain.is_valid())
