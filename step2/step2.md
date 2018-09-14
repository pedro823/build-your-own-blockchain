Let's break our current blockchain.

```python

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

```

Why does it break?
Because each block is independent of the other.
Since we want to create an unalterable blockCHAIN, we need to change
something about the blocks.
In particular, we're going to add the hash of the previous block alongside it.

```python
import hashlib

class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, data, previous_hash):
        self.data = str(data)
        self.previous_hash = previous_hash # little change here
        self.hash = self.calculate_hash()

    def is_valid(self):
        return self.data is not None and self.hash == self.calculate_hash()

    def calculate_hash(self):
        h = hashlib.sha256()
        h.update(bytes(self.data, 'utf8'))
        h.update(bytes(self.previous_hash, 'ascii')) # Also considers it in the hash
        return h.hexdigest()

```

blockchain also changes a bit:

```python
from block import Block

class Blockchain:
    ''' Will hold a stream of blocks. '''
    def __init__(self):
        self.blockchain = [self.genesis_block()]

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

    def add_block(self, block):
        if not isinstance(block, Block):
            raise Exception('add_block: must be a block')
        self.blockchain.append(block)
```

now for the breaking test (altered a bit):

```python
from block import Block
from blockchain import Blockchain

if __name__ == '__main__':
    blockchain = Blockchain()
    block_a = Block('information a', blockchain.genesis_block().hash)
    block_b = Block('information b', block_a.hash)
    blockchain.add_block(block_a)
    blockchain.add_block(block_b)
    # Remember: blockchain.blockchain is our list
    # of blocks
    print(blockchain.blockchain)

    print(blockchain.is_valid()) # Should return True.
    # Tampers with the ORDER of the blocks.
    blockchain.blockchain = blockchain.blockchain[::-1]
    print(blockchain.blockchain) # Oh no, the blockchain list is now reversed!
    print(blockchain.is_valid()) # This now returns False!
```

We should make this concept a bit more user-friendly:

```python
import hashlib

class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, data, previous_hash=''): # previous_hash is optional
        self.data = str(data)
        self.hash = self.calculate_hash()
        self.previous_hash = previous_hash

    def is_valid(self):
        return self.data is not None and self.hash == self.calculate_hash()

    def calculate_hash(self):
        h = hashlib.sha256()
        h.update(bytes(self.data, 'utf8'))
        h.update(bytes(self.previous_hash, 'ascii'))
        return h.hexdigest()

```

the Blockchain class should handle the setting of the previous hash.

```python
from block import Block

class Blockchain:
    ''' Will hold a stream of blocks. '''
    def __init__(self):
        self.blockchain = [self.genesis_block()]

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

    def add_block(self, block):
        if not isinstance(block, Block):
            raise Exception('add_block: must be a block')
        block.previous_hash = self.blockchain[-1].hash # Sets previous hash
        block.hash = block.calculate_hash() # Hash must be recalculated
        self.blockchain.append(block)
```

Now the breaking test is written like before now:

```python
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

    print(blockchain.is_valid()) # returns True.
    # Tampers with the ORDER of the blocks.
    blockchain.blockchain = blockchain.blockchain[::-1]
    print(blockchain.blockchain)
    print(blockchain.is_valid()) # returns False!
```
