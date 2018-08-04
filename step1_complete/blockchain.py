from block import Block

class Blockchain:
    ''' Will hold a stream of blocks. '''
    def __init__(self):
        self.blockchain = [self.genesis_block()]

    def genesis_block(self):
        return Block('Genesis')

    def is_valid(self):
        for block in self.blockchain:
            if not block.is_valid():
                return False
        return True

    def add_block(self, block):
        if not isinstance(block, Block):
            raise Exception('add_block: must be a block')
        self.blockchain.append(block)
