import yaml
from config.path import DATA_PATH, CONFIG_PATH


def read_yaml(file):
    with open(DATA_PATH/file, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)

def write_yaml(file, data):
    with open(DATA_PATH/file, 'w', encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False)

def read_config():
    with open(CONFIG_PATH, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)