import hashlib

class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, data, previous_hash=''): # previous_hash is optional
        self.data = str(data)
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def is_valid(self):
        return self.data is not None and self.hash == self.calculate_hash()

    def calculate_hash(self):
        h = hashlib.sha256()
        h.update(bytes(self.data, 'utf8'))
        h.update(bytes(self.previous_hash, 'ascii')) # Takes previous hash in consideration
        return h.hexdigest()
