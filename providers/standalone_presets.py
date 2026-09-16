import json

from random import choice
from pathlib import Path


CONFIG_PATH = Path(__file__).parent.parent / "config.json"


def get_preset_image(app: dict | None = None) -> str:
    apps:dict = {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as config:
        config_data = json.load(config)
        for standalone_app in config_data["standalone"]:
            app = dict(
                id = standalone_app["id"],
                name = standalone_app["name"],
                path = standalone_app["path"],
                provider = "standalone",
            )
    print(apps.values["path"])
get_preset_image()