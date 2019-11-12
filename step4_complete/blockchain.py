from block import Block, Transaction

class Blockchain:
    ''' Will hold a stream of blocks. '''
    def __init__(self, difficulty = 4):
        # Added: Blockchain difficulty
        self.difficulty = difficulty
        self.blockchain = [self.genesis_block()]
        self.pending_transactions = []

    def genesis_block(self):
        return Block([], difficulty=0, previous_hash='0' * 64) # little change here

    def is_valid(self):
        for block in self.blockchain:
            if not block.is_valid():
                return False

        for i in range(1, len(self.blockchain)):
            if self.blockchain[i].previous_hash != self.blockchain[i - 1].hash:
                return False

        return True

    def add_pending(self, transaction: Transaction):
        self.pending_transactions.append(transaction)

    def build_block(self):
        if len(self.pending_transactions) == 0:
            raise Exception('build_block: no transactions to build a block from')

        block = Block(self.pending_transactions, self.difficulty, self.blockchain[-1].hash)
        block.mine()
        self.pending_transactions = []
        self.blockchain.append(block)

    def check_balance(self, wallet_address: str):
        balance = 0

        for block in self.blockchain:
            for transaction in block.transactions:
                if transaction.from_address == wallet_address:
                    balance -= transaction.amount
                
                if transaction.to_address == wallet_address:
                    balance += transaction.amount
        
        return balance
