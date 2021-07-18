# Utilities for managing known nodes in the network (e.g., broadcasting blocks, querying nodes, etc.).

from typing import Dict, List, Union

import requests

import config
from config import cfg
from block import Block

Endpoint = Dict[str, Union[str, int]]

hostname: str = cfg["endpoint"]["hostname"]
port: int = cfg["endpoint"]["port"]

class Node():
    hostname: str
    port: int

    def __init__(self, hostname: str, port: int = None):
        self.hostname = hostname
        self.port = port

    @property
    def url(self) -> str:
        return self.hostname + (f":{self.port}" if self.port is not None else "")
    
    def get_block(self, index: int) -> Block:
        "Requests the block at the specified index from the node."
        response = requests.get(f"{self.url}/query", params={'index': index})
        return Block(**response.json())
    
    def issue_block(self, block: Block):
        "Issues the provided block to the node."
        requests.post(f"{self.url}/issue", json={"source": {"host": hostname, "port": port}, "block": block.__dict__})
    
    def request_network(self) -> List["Node"]:
        "Requests all known nodes in the network from this node."
        # TODO: Add error handling.
        response = requests.get(f"{self.url}/network")
        network = [Node(**node) for node in response.json()]
        network.append({"hostname": self.hostname, "port": self.port}) # Add the queried node to the network.
        network.remove(cfg["endpoint"]) # Remove ourselves from the network.
        return network

network: List[Node] = [Node(**endpoint) for endpoint in cfg["network"]]

def broadcast(block: Block, exclude: List[Endpoint] = []):
    "Broadcasts the provided block to all nodes in the network."
    for node in network:
        # TODO: Add error handling.
        if node not in exclude:
            node.issue_block(block)

def add_node(endpoint: Endpoint):
    if endpoint not in network:
        network.append(Node(**endpoint))
        cfg["network"] = network
        config.save(cfg)

def absorb_network(node: Node):
    "Downloads the network known by a particular node and absorbs it into this node's network knowledge."
    for endpoint in node.request_network():
        add_node(endpoint)

# Download the network from the first node provided.
absorb_network(network[0])
