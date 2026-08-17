import requests
import json

from pathlib import Path


STEAM_DIRECTORY = Path("D:/Steam/steamapps")


def get_installed_apps() -> list:
    apps = []
    
    for manifest in STEAM_DIRECTORY.glob("appmanifest_*.acf"):
        app_id = int(manifest.stem.split("_")[1])
        apps.append(app_id)

    return apps


def get_app_data(app_id: int) -> dict | None:
    
    response = requests.get(
        f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    )
    data = response.json()
    app = data[str(app_id)]["success"]
    
    if app: 
        app_name = data[str(app_id)]["data"]["name"]
        app_header_image = data[str(app_id)]["data"]["header_image"]
        
        app_data = dict(
            name = app_name, 
            id = app_id, 
            image = app_header_image
        )
        return app_data
    else:
        print(f"Skipped: {app_id}")
        return None


def get_apps(app_list: list):
    apps = []
    for app in app_list:
        app_data = get_app_data(app)
        if app_data is not None:
            apps.append(app_data)
    return apps
    
