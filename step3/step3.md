Let's break our blockchain once again.

```python
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

```
Why didn't the `is_valid()` function detect that something was wrong?  
Because we also went to every block that comes after the tampered one and _fixed_
the `previous_hash` of each.

How do we fix this? Establishing some difficulty barriers to the blockchain:

- It should be **easy** to check if a chain is valid or not.
- It should be **relatively easy** to insert a block in a blockchain.
- It should be **very hard** to tamper with a block in the middle of the chain.

We'll add a feature that *kinda* solves those conditions:  
Proof of work.

What that means: inserting a block into the chain requires solving a computational problem;
checking if a block is correctly inserted into the chain requires checking if the
computational problem was solved correctly; and
tampering with a block in the middle of the chain requires solving the problem for that block
and for every block that comes after it.

Our proof of work will be simple: requiring the hash of the block to start with an amount of zeros.
**TODO**

```python

```