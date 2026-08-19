from core import server


def main():
    print("Up and running")

    http_server = server.create_server()
    http_server.serve_forever()


if __name__ == "__main__":
    main()
