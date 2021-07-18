# Exposes a REST API for requesting blocks from the block chain.

from flask import Flask, jsonify, request
import threading

from block import Block
from blockchain import BlockChain, load_blockchain

app = Flask(__name__)

blockchain = load_blockchain()


@app.route("/query", methods=["GET"])
def query():
    """
    Queries the node for a block by the specified index.
    """
    index = int(request.args.get("index"))
    return jsonify(blockchain.blocks[index].__dict__)

@app.route("/issue", methods=["POST"])
def issue():
    """
    Allows third parties to issue a block to this node.
    """
    source = request.json["source"]
    block = request.json["block"]
    blockchain.validate_next_block(source, Block(**block))
    return "", 200

@app.route("/network")
def network():
    """
    Displays all the known nodes in the network.
    """
    return jsonify(list(network.network))

# Initiate block mining in a separate thread.
threading.Thread(target=blockchain.mine, kwargs={"debug": True}).start()

if __name__ == "__main__":
    # Start the Flask app.
    app.run(host="0.0.0.0", port=5000)
