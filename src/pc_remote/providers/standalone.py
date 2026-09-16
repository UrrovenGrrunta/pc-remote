import json 

from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.json"

def make_slug(name: str) -> str:
    slug = ""
    
    for char in name.lower():
        if char.isalnum():
            slug += char
        elif (
            char == " "
            and slug
            and slug[-1] != "-"
        ):
            char = "-"

    return slug.rstrip("-")


def get_apps() -> list[dict]:
    
    apps = []
    with open(CONFIG_PATH, 'r', encoding="utf-8") as config:
        config_data = json.load(config)
        for standalone_app in config_data["standalone"]:
            app = dict(
                id=standalone_app["id"],
                name=standalone_app["name"],
                provider="standalone",
            )
            apps.append(app)
    return apps
