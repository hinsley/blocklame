# Defines a class that represents a block in the blockchain.

import hashlib

import mining

DATA_LENGTH = 1024

class Block():
    index: int
    timestamp: int
    data: str
    nonce: int
    
    prev_hash: str

    def __init__(self, index, data, prev_hash=hashlib.sha256("".encode("utf-8")).hexdigest(), timestamp=0, nonce=0):
        self.index = int(index)
        self.prev_hash = prev_hash
        self.timestamp = int(timestamp)
        self.update_data(data)
        self.nonce = int(nonce)

    def __str__(self):
        return f"{self.index} {self.timestamp} {self.data} {self.prev_hash} {self.nonce}"

    def hash(self):
        return hashlib.sha256(str(self).encode("utf-8")).hexdigest()

    def is_valid(self):
        """
        Determines whether the block's hash meets the current difficulty
        requirement.
        """
        return self.hash().startswith("0" * mining.hash_difficulty(self.index))

    def increment_nonce(self):
        self.nonce += 1

    def update_data(self, data):
        self.data = Block.pad_data(data)

    @classmethod
    def pad_data(cls, data: str):
        """
        Pads the data with null bytes or truncates to reach a length of 1024
        characters.
        """
        return data.ljust(DATA_LENGTH, "\0")[:DATA_LENGTH]
