## Create your own blockchain in python!

Step 1: The block and blockchain

```python

class Block:
    ''' Will hold a block of data and its validation. '''
    pass


class Blockchain:
    ''' Will hold a stream of blocks. '''
    pass

```

Initialize the block.

```python

class Block:
  ''' Will hold a block of data and its validation. '''

    def __init__(self, data):
        self.data = str(data)

    def is_valid(self):
        return self.data is not None # Always True

```

Initialize the blockchain.

```python

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

```

Put hash in block.

```python

import hashlib

class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, data):
        self.data = str(data)
        self.hash = self.calculate_hash()

    def is_valid(self):
        return self.data is not None and self.hash == self.calculate_hash()

    def calculate_hash(self):
        h = hashlib.sha256()
        h.update(bytes(self.data, 'utf8'))
        return h.hexdigest()

```

allow adding to the blockchain.

```python
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
```

test!

```python
from block import Block
from blockchain import Blockchain

if __name__ == "__main__":
    blockchain = Blockchain()
    block = Block('random data here')
    print(blockchain.is_valid()) # Should return True!
    blockchain.add_block(block)
    print(blockchain.is_valid()) # Should return True again.
    block.data = 'tampered data!!!'
    print(blockchain.is_valid()) # Oh no, block was tampered! Should return False

```
