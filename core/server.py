import os
import json
import providers.steam as steam
import launchers

from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        match self.path:
            case "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                with open(
                    "static/index.html",
                    "r",
                    encoding="utf-8",
                ) as file:
                    html = file.read()
                    self.wfile.write(html.encode("utf-8"))

            case "/script.js":
                self.send_response(200)
                self.send_header(
                    "Content-type",
                    "text/javascript",
                )
                self.end_headers()

                with open(
                    "static/script.js",
                    "r",
                    encoding="utf-8",
                ) as file:
                    js = file.read()
                    self.wfile.write(js.encode("utf-8"))

            case "/style.css":
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()

                with open(
                    "static/style.css",
                    "r",
                    encoding="utf-8",
                ) as file:
                    css = file.read()
                    self.wfile.write(css.encode("utf-8"))

            case path if path.startswith("/images/"):
                image_name = path.removeprefix("/images/")
                image_path = os.path.join(
                    "static",
                    "images",
                    image_name,
                )

                if not os.path.isfile(image_path):
                    self.send_response(404)
                    self.end_headers()
                    return

                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.end_headers()

                with open(image_path, "rb") as file:
                    self.wfile.write(file.read())

            case "/launch/gr7":
                launchers.launch_gr7()
                self.send_response(200)
                self.end_headers()

            case "/launch/osu":
                launchers.launch_osu()
                self.send_response(200)
                self.end_headers()

            case "/launch/ubuntu":
                launchers.launch_ubuntu()
                self.send_response(200)
                self.end_headers()

            case "/apps":
                apps = steam.get_apps(steam.get_installed_apps())

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(apps).encode("utf-8"))

            case path if path.startswith("/launch/"):
                app_id = int(path.removeprefix("/launch/"))
                launchers.launch_app(app_id)

                self.send_response(200)
                self.end_headers()

            case _:
                self.send_response(404)
                self.end_headers()


def create_server():
    host = "100.85.81.84"
    port = 8000

    return HTTPServer((host, port), RequestHandler)
