import json


def get_data():
    with open('data.json', 'r') as f:
        return json.loads(f.read())


def safe_data(data):
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))
