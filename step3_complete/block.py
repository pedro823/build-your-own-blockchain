import hashlib

class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, data, difficulty: int, previous_hash=''):
        self.data = str(data)
        self.difficulty = difficulty
        self.previous_hash = previous_hash
        self.nonce = 0

    @property
    def hash(self):
        h = hashlib.sha256()
        h.update(bytes(self.data, 'utf8'))
        h.update(bytes(self.previous_hash, 'ascii'))
        h.update(bytes(str(self.nonce), 'ascii'))
        return h.hexdigest()

    def is_valid(self):
        return self.data is not None \
               and self.hash.startswith('0' * self.difficulty)

    def mine(self):
        while not self.is_valid():
            self.nonce += 1