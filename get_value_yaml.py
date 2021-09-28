import yaml
from yaml.loader import FullLoader

def get_value(value):
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=FullLoader)
    return data[value]
