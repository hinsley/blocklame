import json

filename = "config.json"

cfg = None
with open(filename, "r") as f:
    cfg = json.load(f)

def save(config):
    with open(filename, "w") as f:
        json.dump(config, f)
