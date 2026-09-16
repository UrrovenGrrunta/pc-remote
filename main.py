from core import server
from core import game_cache

def main():
    game_cache.load_games_cache()
    print("Up and running")

    http_server = server.create_server()
    http_server.serve_forever()


if __name__ == "__main__":
    main()
