from pc_remote.core import game_cache, server


def main() -> None:
    game_cache.load_games_cache()
    print("Up and running")

    http_server = server.create_server()
    http_server.serve_forever()
