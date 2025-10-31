import json

with open("config.json", 'r') as c:
    config = json.load(c)

def load(value):
    return config["value"]
