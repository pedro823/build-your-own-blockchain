from block import Block

class Blockchain:
    ''' Will hold a stream of blocks. '''
    def __init__(self, difficulty = 4):
        self.blockchain = [self.genesis_block()]
        self.difficulty = difficulty

    def genesis_block(self):
        return Block('Genesis', '0' * 64) # little change here

    def is_valid(self):
        for block in self.blockchain:
            if not block.is_valid():
                return False
        # also checks for matching previous hashes
        for i in range(1, len(self.blockchain)):
            if self.blockchain[i].previous_hash != self.blockchain[i - 1].hash:
                return False
        return True

    def create_block(self, data):
        

    def add_block(self, block):
        if not isinstance(block, Block):
            raise Exception('add_block: must be a block')
        block.previous_hash = self.blockchain[-1].hash # Sets previous hash
        block.hash = block.calculate_hash()
        self.blockchain.append(block)
