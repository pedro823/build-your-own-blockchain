import hashlib

class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, data, difficulty, previous_hash=''): # ADDED: difficulty
        self.data = str(data)
        self.hash = self.calculate_hash()
        self.difficulty = difficulty
        self.previous_hash = previous_hash
        self.nonce = 0 # nonce := Number used once

    def is_valid(self):
        # is_valid checks if hash starts with
        return self.data is not None \
               and self.hash == self.calculate_hash() \
               and self.hash.startswith('0' * self.difficulty, beg=0)

    def calculate_hash(self):
        h = hashlib.sha256()
        h.update()
        h.update(bytes(self.data, 'utf8'))
        h.update(bytes(self.previous_hash, 'ascii'))
        return h.hexdigest()
