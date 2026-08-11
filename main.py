import os

from http.server import BaseHTTPRequestHandler, HTTPServer

APPS = {
    "cs2": 730,
    "gd": 322170,
    "TBOI": 250900,
    "ets_2": 227300,
    "phasmo": 739630,
    "ADOFAI": 977950,
    "vcd": 246900,
    "cloverpit": 3314790,
    "starrupture": 1631270,
    "satisfactory": 526870,
    "creepy_support": 3685900,
    "passport_blyat": 239030,
    "graveyard_keeper": 599140,
    "everlasting_summer": 331470,
    "vcd_shadow_warrior": 255520,
    "deep_rock_galactic": 548430,
    "vcd_santas_rampage": 265210,
}


def launch_osu():
    os.startfile(r"C:\Users\timbr\Desktop\OTD\OpenTabletDriver.UX.Wpf.exe")
    os.startfile(r"D:\OSUSTBL\osu!.exe")


def launch_gr7():
    os.startfile(r"C:\Native Instruments\Guitar Rig 7/Guitar Rig 7.exe")


def launch_app(app_name: str):
    app_id = APPS[app_name]
    os.startfile(f"steam://rungameid/{app_id}")


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        match self.path:
            case "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open("static/index.html", "r", encoding="utf-8") as file:
                    html = file.read()
                    self.wfile.write(html.encode("utf-8"))

            case "/script.js":
                self.send_response(200)
                self.send_header("Content-type", "text/javascript")
                self.end_headers()
                with open("static/script.js", "r", encoding="utf-8") as file:
                    js = file.read()
                    self.wfile.write(js.encode("utf-8"))

            case "/style.css":
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                with open("static/style.css", "r", encoding="utf-8") as file:
                    css = file.read()
                    self.wfile.write(css.encode("utf-8"))

            case path if path.startswith("/images/"):
                image_name = path.removeprefix("/images/")
                image_path = os.path.join("static", "images", image_name)

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
                launch_gr7()
                self.send_response(200)
                self.end_headers()
                
            case "/launch/osu":
                launch_osu()
                self.send_response(200)
                self.end_headers()

            case path if path.startswith("/launch/"):
                app_name = path.removeprefix("/launch/")
                launch_app(app_name)
                self.send_response(200)
                self.end_headers()

            case _:
                self.send_response(404)
                self.end_headers()


def main():
    print("Up and running")
    host: str = "100.85.81.84"
    port: int = 8000
    server = HTTPServer((host, port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
