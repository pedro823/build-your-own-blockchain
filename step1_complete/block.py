import hashlib

class Block:
    ''' Will hold a block of data and its validation. '''

    def __init__(self, data):
        self.data = str(data)
        self.hash = self.calculate_hash()

    def is_valid(self):
        return self.data is not None and self.hash == self.calculate_hash()

    def calculate_hash(self):
        h = hashlib.sha256()
        h.update(bytes(self.data, 'utf8'))
        return h.hexdigest()
