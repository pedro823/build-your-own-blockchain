Until this point, we haven't made any assumptions to our blockchain:
It has stored arbitrary data in its blocks.

From now on, we're going to assume that our blockchain will handle
**transactions**. That is, we're building a _cryptocurrency_ from now on.

Now that we have this assumption, we can make some changes to our data.
First of all, let's add a `Transaction` class to our `block.py`:

```python
class Transaction:
    def __init__(self, from_address: str, to_address: str, amount: float):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount

    def __repr__(self):
        return f'<Transaction from={self.from_address} to={self.to_address} amount={self.amount}>'
```

This is just a basic class that will hold information, and is quite self explanatory: 
The transaction will hold the address which the coins left (`from_address`), the address that the coins went to (`to_address`)
and how many coins made the trip (`amount`).  
It also has a neat string representation that will be useful for calculating the block hash later on.

Now, since our blockchain will handle transactions, 
**each of our blocks will contain a list of transactions that happened**.

Our block class has therefore changed:
```python
class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, transactions: list, difficulty: int, previous_hash=''):
        self.transactions = transactions # transactions is a list of Transaction classes.
        self.difficulty = difficulty
        self.previous_hash = previous_hash
        self.nonce = 0

    @property
    def hash(self):
        h = hashlib.sha256()
        h.update(bytes(str(self.transactions), 'utf8'))
        h.update(bytes(self.previous_hash, 'ascii'))
        h.update(bytes(str(self.nonce), 'ascii'))
        return h.hexdigest()

    def is_valid(self):
        return self.transactions \
               and self.hash.startswith('0' * self.difficulty)

    def mine(self):
        while not self.is_valid():
            self.nonce += 1

    def __repr__(self):
        # We don't need to show the whole hash -- showing the last 6 digits is more than plenty for our purposes.
        return f'<Block transactions={self.transactions} hash={self.hash[-6:]} nonce={self.nonce}>'
```

some things to note:

1. Inside the `is_valid` function, the first condition that is checked is that `self.transactions` is truthy.
  That is a shortcut to check both that `self.transactions` is not `None` and not an empty list, since
  `bool(self.transactions)` returns `False` if `self.transactions == []`. This is very Javascript-like
  even though the behaviour is very different, so never overuse this hack.

2. On the `hash` property function, one subtle thing that you may have missed is that
  `self.transactions` is being converted to a string before being converted to bytes.
  When that list of transactions gets converted to a string, all the transactions get
  converted to strings as well, calling the `__repr__` function of every transaction.
  **This is very important**, as we need to consider the data _inside_ the transactions
  for the final hash of the block.

Our blockchain class gets some little changes as well.
The idea is that our blockchain will contain all the pending transactions that weren't included
in a block yet, and then pack them all into a block, mining it afterwards. 

```python
from block import Block, Transaction

class Blockchain:
    
    def __init__(self, difficulty = 4):
        ...
        self.pending_transactions = [] # We'll now hold all pending transactions

    def genesis_block(self):
        return Block([], difficulty=0, previous_hash='0' * 64) # little change here

    ...

    def add_pending(self, transaction: Transaction):
        self.pending_transactions.append(transaction)

    def build_block(self):
        if len(self.pending_transactions) == 0:
            raise Exception('build_block: no transactions to build a block from')

        block = Block(self.pending_transactions, self.difficulty, self.blockchain[-1].hash)
        block.mine()
        self.pending_transactions = []
        self.blockchain.append(block)
```

Cool. Now we have a very rudimental way to add transactions to the blockchain. We can test that:
our `blockchain_test.py` goes like this:

```python
from block import Block, Transaction
from blockchain import Blockchain

bc = Blockchain(difficulty=4)

bc.add_pending(Transaction('my_address', 'your_address', 5.0))
bc.add_pending(Transaction('your_address', 'my_address', 2.0))
bc.add_pending(Transaction('your_address', 'other_address', 3.0))

bc.build_block()

for block in bc.blockchain:
    print(block)
```

The result should be that there is 2 blocks: The genesis block and a block containing 3 transactions.

For now, our wallets are just a simple string containing an unique identifier. In our example,
they are `my_address`, `your_address`, and `other_address`.

We can create a function that checks the balance of a given ID. The simplest way to
implement it is to create a procedure that checks every transaction that ever existed,
checking if the ID was mentioned in the `from_address` or in the `to_address`.  
If it was mentioned in the `from_address`, the coins left the wallet, and therefore we subtract from the balance.
Analogously, if it was mentioned in the `to_address`, the coins went to this wallet, and therefore we add to the balance.

```python
class Blockchain:
    ...
    def check_balance(self, wallet_address: str):
        balance = 0

        # We need to loop on every block, since each block contains many transactions.
        for block in self.blockchain:
            for transaction in block.transactions:
                if transaction.from_address == wallet_address:
                    balance -= transaction.amount
                
                if transaction.to_address == wallet_address:
                    balance += transaction.amount
        
        return balance
```

we can add to our test to see it working in practice. Our test therefore becomes:

```python
from block import Block, Transaction
from blockchain import Blockchain

bc = Blockchain(difficulty=4)

bc.add_pending(Transaction('my_address', 'your_address', 5.0))
bc.add_pending(Transaction('your_address', 'my_address', 2.0))
bc.add_pending(Transaction('your_address', 'other_address', 3.0))

bc.build_block()

for block in bc.blockchain:
    print(block)

for address in ['my_address', 'your_address', 'other_address']:
    print(address, bc.check_balance(address))
```

That's it for this step!