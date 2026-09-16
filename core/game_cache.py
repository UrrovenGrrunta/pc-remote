import providers.steam as steam
import providers.hydra as hydra


apps_cache: list[dict] = []
hydra_games_cache: list[dict] = []


def load_games_cache() -> list[dict]:
    global apps_cache
    global hydra_games_cache

    hydra_games = hydra.get_hydra_games()
    hydra_apps = hydra.get_apps(hydra_games)

    steam_apps = steam.get_apps(
        steam.get_installed_apps()
    )

    hydra_games_cache = hydra_games
    apps_cache = hydra_apps + steam_apps

    return apps_cache