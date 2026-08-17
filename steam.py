from pathlib import Path


STEAM_DIRECTORY = Path("D:/Steam/steamapps")


def get_installed_apps():
    with (STEAM_DIRECTORY / "libraryfolders.vdf").open(
        "r",
        encoding="utf-8",
    ) as file:
        apps = []
        in_apps = False

        for line in file:
            line = line.strip().strip('"')

            if line == "apps":
                in_apps = True

            if in_apps:
                if line == "}":
                    in_apps = False
                else:
                    parts = line.split('"')

                    try:
                        app_id = int(parts[0])
                        apps.append(app_id)
                    except ValueError:
                        continue

    return apps
