# Utilities for managing known nodes in the network (e.g., broadcasting blocks, querying nodes, etc.).

from typing import Set

import requests

from config import cfg
from block import Block

# TODO: Add a way to find other nodes in the network.

hostname: str = cfg["endpoint"]["hostname"]
port: int = cfg["endpoint"]["port"]

class Node():
    ip: str
    port: int

    def __init__(self, ip: str, port: int=None):
        self.ip = ip
        self.port = port

    @property
    def url(self) -> str:
        return self.ip + (f":{self.port}" if self.port is not None else "")
    
    def get_block(self, index: int) -> Block:
        "Requests the block at the specified index from the node."
        response = requests.get(f"{self.url}/query", params={'index': index})
        return Block(**response.json())
    
    def issue_block(self, block: Block):
        "Issues the provided block to the node."
        requests.post(f"{self.url}/issue", json={"source": {"host": hostname, "port": port}, "block": block.__dict__})

network: Set[Node] = set()

def broadcast(block: Block):
    "Broadcasts the provided block to all nodes in the network."
    for node in network:
        node.issue_block(block)
