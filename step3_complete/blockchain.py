from block import Block

class Blockchain:
    ''' Will hold a stream of blocks. '''
    def __init__(self, difficulty = 4):
        # Added: Blockchain difficulty
        self.difficulty = difficulty
        self.blockchain = [self.genesis_block()]

    def genesis_block(self):
        return Block('Genesis', difficulty=0, previous_hash='0' * 64) # little change here

    def is_valid(self):
        for block in self.blockchain:
            if not block.is_valid():
                return False

        for i in range(1, len(self.blockchain)):
            if self.blockchain[i].previous_hash != self.blockchain[i - 1].hash:
                return False

        return True

    def add_data(self, data):
        # We'll change to add data so that 
        # only the Blockchain class handles blocks
        if data is None:
            raise Exception('add_data: data must not be None')
        
        block = Block(data, self.difficulty, self.blockchain[-1].hash)
        block.mine()
        self.blockchain.append(block)
