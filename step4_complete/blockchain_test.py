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