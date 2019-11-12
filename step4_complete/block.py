import hashlib

class Transaction:
    def __init__(self, from_address: str, to_address: str, amount: float):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount

    def __repr__(self):
        return f'transaction from={self.from_address} to={self.to_address} amount={self.amount}'

class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, transactions: list, difficulty: int, previous_hash=''):
        self.transactions = transactions
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
        return f'Block transactions={self.transactions} hash={self.hash[-6:]} nonce={self.nonce}'