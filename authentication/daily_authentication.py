import json
import os

def update_access_token(new_token):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_dir, "config.json")

    # Read
    with open(path, "r") as file:
        data = json.load(file)

    # Modify
    data[0]["access_token"] = new_token

    # Write
    with open(path, "w") as file:
        json.dump(data, file, indent=2)

    return data[0]