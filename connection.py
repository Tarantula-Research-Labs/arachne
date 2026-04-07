import json

def load_config():
    with open("./config.json", "r") as file:
        data = json.load(file)
    return data[0]

class Connection:
    def __init__(self):
        self._data = load_config()

    def get(self, key):
        return self._data.get(key)


