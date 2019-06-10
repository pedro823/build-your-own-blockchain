Bear with me, this step is kind of long!


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
            # Also change the previous hash of the next block, if exists
            blockchain.blockchain[idx + 1].previous_hash = block.hash

    print([block.data for block in blockchain.blockchain]) # Oh boy! We've tampered with the data of a block!
    print(blockchain.is_valid()) # And the validating function didn't detect this!

```
Why didn't the `is_valid()` function detect that something was wrong?  
Because we also went to every block that comes after the tampered one and _fixed_
the `previous_hash` of each.

**How do we fix this?** Establishing some difficulty barriers to the blockchain:

- It should be **easy** to check if a chain is valid or not.
- It should be **very hard** to tamper with a block in the middle of the chain.

We'll add a feature that solves those conditions: making it hard to **insert** a block in the blockchain.  

### Proof of work

What that means: inserting a block into the chain requires solving a computational problem;
checking if a block is correctly inserted into the chain requires checking if the
computational problem was solved correctly; and
tampering with a block in the middle of the chain requires solving the problem for that block
and for every block that comes after it.

Our proof of work will be simple: requiring the hash of the block to start with an amount of zeros.

```python
def is_valid(self):
    # is_valid checks if hash starts with difficulty amount of zeroes.
    return self.data is not None \
            and self.hash == self.calculate_hash() \
            and self.hash.startswith('0' * self.difficulty)
```

Let's understand that bit by bit. Pun intended.

Our hash of choice for this blockchain is SHA-256: A 256-bit digest that looks random.
`self.hash` is actually a string containing the hexdump of those 256 bits. A binary number can
be easily encoded into a hexadecimal number because every hexadecimal digit fits exactly 4 binary digits. 
Read more about this [here](https://en.wikipedia.org/wiki/Hexadecimal).

Anyway, here's what a digest may look like:
```
7e59270e9c99be61444f1c3199c83548c12d436cbc9a0b1431422baa1d843313
```

But let's focus first on bits, not hexadecimals.

Question: **How many possible SHA-256 hashes exist?** Well, there's 256 bits of output, 
each bit can assume 2 possible states, therefore there are 2^256 possible hash outputs.
```
1 0 1 1 0 0 1 0 0 0 ...
^
2 options: 1 or 0
256 choices of 2 states: 2^256 total possible states
```

Now, **How many SHA-256 hashes start with a zero?** Since the first number has to start
with a zero, we have 255 bits left to fiddle with. 
```
0 0 1 0 0 1 0 0 0 0 ...
^ ^
| 2 options: 1 or 0
| 255 choices of 2 states: 2^255 total possible states
|
Fixed

```

That means we can get 2^255 possible hashes. 2^255 out of 2^256 hashes start with a zero or,
in other words, **Half of all SHA-256 hashes start with a zero**.

Once again, **How many SHA-256 hashes start with two zeroes?** Now, the two first numbers
are locked in. With the same logic, there are 2^254 possible hashes. That is, 
**A quarter of all SHA-256 hashes start with two zeroes**.

In fact, **Every zero you require at the start of the hash decreases the quantity of hashes by half**.

Now, what about the hexadecimal digest?  
Since every hexadecimal digit can fit 4 binary digits, requiring the digest to start with
a zero actually means requiring the hash to start with 4 zeroes, reducing the possible hashes
by a factor of 16.

Once again, this is achieved by this check:
```python
self.hash.startswith('0' * self.difficulty)

# with difficulty 3,
# one such possible hash is
# 000b493d48364afe44d11c0165cf470a4164d1e2609911ef998be868d46ade3d
```

So, by creating this check, we're **restricting** the possible blocks that can exist: There can only
be blocks which hashes start with `self.difficulty` amount of zeroes. However, this also restricts
the data that we can put in the blocks, because it needs to generate a complying hash. That is not
what we want.

So, to solve that situation, we also add a variable that will add entropy to the hash. We'll call it
`nonce`, which means `number used only once` in cryptography.

Our Block class will look like this:
```python
class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, data, difficulty: int, previous_hash=''): # ADDED: difficulty, an integer
        self.data = str(data)
        self.difficulty = difficulty # difficulty stays here
        self.previous_hash = previous_hash
        self.nonce = 0 # The nonce is initialized over here
        self.hash = self.calculate_hash()

    def is_valid(self):
        return self.data is not None \
               and self.hash == self.calculate_hash() \
               and self.hash.startswith('0' * self.difficulty)

    def calculate_hash(self):
        h = hashlib.sha256()
        h.update(bytes(self.data, 'utf8'))
        h.update(bytes(self.previous_hash, 'ascii'))
        h.update(bytes(str(self.nonce), 'ascii')) # We also use the nonce in the hash calculation
        return h.hexdigest()
```

This nonce will be used for "fixing" the hash.  
We put data in the block, and it'll generate a hash. If that hash satisfies the difficulty checked
in `block.is_valid()`, then great! But most probably it won't. But that's okay, we change the nonce
and try again. We do that until we get a valid block.

```python
while not block.is_valid():
    block.nonce += 1
    block.hash = block.calculate_hash()
```

This process is literally what the cool kids call "**mining** a block". In Bitcoin, for example, a
batch of transactions is loaded into a block (which would represent our `data` property) and then
different miners try to find a `nonce` for the block so that it satisfies the current difficulty.

We'll add that snippet of code to the block class:

```python
class Block:

    # ...

    def mine(self):
        while not self.is_valid():
            self.nonce += 1
            self.hash = self.calculate_hash()
```

While we're here, we can throw away the hash that we calculate at the beginning of the Block's life,
as it **does not provide any extra security**. our secure link is in `self.calculate_hash()` starting
with x amount of zeroes.

```python
class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, data, difficulty: int, previous_hash=''): # ADDED: difficulty, an integer
        self.data = str(data)
        self.difficulty = difficulty
        self.previous_hash = previous_hash
        self.nonce = 0
        # removed self.hash over here

    def is_valid(self):
        # removed the self.hash == self.calculate_hash() over here
        return self.data is not None \
               and self.calculate_hash().startswith('0' * self.difficulty)

    def calculate_hash(self):
        h = hashlib.sha256()
        h.update(bytes(self.data, 'utf8'))
        h.update(bytes(self.previous_hash, 'ascii'))
        h.update(bytes(str(self.nonce), 'ascii')) # We also use the nonce in the hash calculation
        return h.hexdigest()

    def mine(self):
        while not self.is_valid():
            self.nonce += 1
            # removed self.hash over here
```

Now, for bonus points on python code readability: we can make calculate_hash() be a **property** of the Block
class instead of a **method**. We'll use `block.hash` as if it was just a variable bound to `block` even though
it will be a bound function.

```python
class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, data, difficulty: int, previous_hash=''): # ADDED: difficulty, an integer
        self.data = str(data)
        self.difficulty = difficulty
        self.previous_hash = previous_hash
        self.nonce = 0

    @property
    def hash(self):
        # Moved the code from calculate_hash() to here
        h = hashlib.sha256()
        h.update(bytes(self.data, 'utf8'))
        h.update(bytes(self.previous_hash, 'ascii'))
        h.update(bytes(str(self.nonce), 'ascii')) # We also use the nonce in the hash calculation
        return h.hexdigest()

    def is_valid(self):
        # Changed from self.calculate_hash() to self.hash
        return self.data is not None \
               and self.hash.startswith('0' * self.difficulty)

    def mine(self):
        while not self.is_valid():
            self.nonce += 1
```

Our Block class is done for now. We just need to adapt the Blockchain class to comply with 
everything we've done so far. Here we go:

```python
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

```

Let's test it! If you're feeling adventurous, try cranking the blockchain difficulty up some numbers. You'll see it
quickly gets out of hand.

```python
from blockchain import Blockchain

bc = Blockchain(difficulty=4)

for i in range(10):
    bc.add_data(f'data #{i}')

for idx, block in enumerate(bc.blockchain):
    print(f'Block #{idx}: data={block.data} hash={block.hash} nonce={block.nonce}')

print(f'Blockchain.is_valid={bc.is_valid()}')
```

Running this code, you'll see something like this:

```
Block #0: data=Genesis hash=ad121dad74ad17ac777c6225bf64b595309e8d0e6556a97ebeacf18d3ea16b6e nonce=0
Block #1: data=data #0 hash=00007feefe2fafcda991b44528498ef73c4441d1abea258834ef7f347b6c21c4 nonce=7639
Block #2: data=data #1 hash=000099b899c300e3cbde8f8d2c5ac56753e801cf4a7a2f0c252629322a63da77 nonce=80769
Block #3: data=data #2 hash=000065a333ea3117369bdda879070f6d367e4385b43f9da8a4a4cec13d0b9513 nonce=7951
Block #4: data=data #3 hash=00007625d692ebb3516cbba2f5d1a4725b057cc700d47b50d279f5b114412a42 nonce=137459
Block #5: data=data #4 hash=0000c5bc01ab2f670112459f3e3d1916ae38208df5c6b998aa7eab19bd070d81 nonce=152972
Block #6: data=data #5 hash=000077e39bc61324cff97da894c5381bc12e956c78188dfa6395f918b43b0790 nonce=64509
Block #7: data=data #6 hash=000045cdc119c0166197e5da5c5ac19866ca7300cb0e9e231c82763aa7f4430b nonce=37676
Block #8: data=data #7 hash=000048560cfeac06984886ec71b48ff8a6dca35e017fb8741dcac5ac157fb0a4 nonce=149822
Block #9: data=data #8 hash=0000d21fc755839dcaebb981e75b6ec5c577269db709ec7a240164284ca2bc2e nonce=1936
Block #10: data=data #9 hash=00008254624324866d8ac6d6f9b96855ef5e0fdfac86c4911774afd657835923 nonce=9894
Blockchain.is_valid=True
```

The genesis block is unmined, because its difficulty is set to zero on its creation. All other blocks
were mined, and wow -- the nonces vary from 1936 to 152k!

