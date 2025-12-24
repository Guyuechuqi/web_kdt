from pathlib import Path

current_path = Path(__file__).resolve()
root_path = current_path.parent.parent

CONFIG_PATH = root_path / 'config' / 'config.yaml'
DATA_PATH = root_path / "data"