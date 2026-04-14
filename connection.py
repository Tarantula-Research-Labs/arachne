import os
import json

def load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")

    with open(config_path, "r") as file:
        data = json.load(file)
    return data[0]

class Connection:
    def __init__(self):
        self._data = load_config()

    def get(self, key):
        return self._data.get(key)


