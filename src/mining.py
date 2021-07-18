from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from block import Block

import math
from time import time

def hash_difficulty(index: int) -> int:
    """
    Determines how many zero digits the block hash must begin
    with given the current index.
    :param index: The current index.
    :return: The number of zero digits the hash must begin with.
    """
    try:
        return math.floor(math.log2(index))
    except ValueError:
        return 0

def mine(block: Block):
    """
    Takes a new block and searches for a valid nonce for it.
    :param block: The block to mine.
    """
    while not block.is_valid():
        block.increment_nonce()
    block.timestamp = int(time())
