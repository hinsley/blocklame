from typing import Dict, List, Union
from time import time

from block import Block
from mining import mine
import network

class BlockChain():
    blocks: List[Block]

    def __init__(self):
        self.blocks = [Block(0, "NULLIUS IN VERBA")]
        mine(self.blocks[0])
    
    def mine(self, debug=False):
        "Mines new blocks forever."
        if debug:
            print("Mining...")
        while True:
            self.mine_next_block(f"Block {len(self.blocks)}")
            if debug:
                print(f"Mined block {len(self.blocks)-1}")

    def mine_next_block(self, data: str):
        "Mines a new block and adds it to the chain."
        new_block = Block(len(self.blocks), data, self.blocks[-1].hash())
        mine(new_block)
        self.blocks.append(new_block)
        network.broadcast(new_block)
    
    def validate_next_block(self, source: Dict[str, Union[str, int]], block: Block) -> bool:
        """
        Validates a new candidate block against the existing local blockchain ledger.
        Discards any existing blocks in the local ledger necessary to maintain continuity.
        Returns True if the block is valid, False otherwise.
        """
        if block.index < len(self.blocks):
            return False # The block originated from an outdated ledger.
        
        sender = network.Node(*source)

        new_blocks = []

        current_block = block
        while True:
            if current_block.index == 0:
                return False # We should never allow revision of block #0.
            new_blocks.insert(0, current_block)
            try:
                if current_block.prev_hash == self.blocks[current_block.index-1].hash():
                    if current_block.timestamp < self.blocks[current_block.index-1].timestamp or \
                       current_block.index-1 != self.blocks[current_block.index-1].index:
                       return False # Continuity is broken.
                    break # Continuity established.
            except IndexError:
                pass # We're covering a gap in the chain, so we can't validate this block yet.
            # We still have a continuity mismatch and need to keep requesting predecessor blocks.
            pred_block = sender.get_block(current_block.index-1)
            # We need to check whether the predecessor block maintains continuity with the block coming after it.
            if current_block.prev_hash != pred_block.hash() or \
               current_block.timestamp < pred_block.timestamp or \
               current_block.index-1 != pred_block.index:
                return False # Consistency broken.
            current_block = pred_block # Consistency maintained.

        # Update our ledger with all new/revised blocks.
        self.blocks = self.blocks[:new_blocks[0].index] + new_blocks
        network.broadcast(block) # Broadcast this new block to all nodes.
        return True
