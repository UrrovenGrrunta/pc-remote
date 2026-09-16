import json

from pc_remote.paths import CONFIG_PATH
from pc_remote.providers import standalone


def create_config():
    config = {
        "standalone": []
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(config, file,indent=4)
        


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = json.load(file)
        
    return config


def ensure_config():
    if not CONFIG_PATH.is_file():
        create_config()

ensure_config()


def add_standalone(
    name: str,
    path: str,
    launch_before: list | None = None
):
    slug = standalone.make_slug(name)
    config = load_config()
    standalone_dict = {
        "id": slug, 
        "name": name,
        "path": path,
        "launch_before": launch_before if launch_before is not None else [],
    }
    config["standalone"].append(standalone_dict)
    
    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4, ensure_ascii=False)
        
