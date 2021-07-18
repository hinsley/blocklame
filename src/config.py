import json

filename = "config.json"

cfg = None
with open(filename, "r") as f:
    cfg = json.load(f)
