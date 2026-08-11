# PC Remote

A small personal remote-control server for a Windows gaming PC.

PC Remote runs a lightweight Python HTTP server on Windows and exposes a mobile-friendly web interface over Tailscale. From a phone browser, the interface can launch installed Steam games and other local applications on the PC.

## Features

- Mobile-friendly game library interface
- Remote access through Tailscale
- Launch Steam games using their Steam AppID
- Launch non-Steam applications from local executable paths
- Custom launch actions, such as starting osu! together with OpenTabletDriver
- Steam artwork for game cards with support for locally hosted images
- No web framework required

## Tech stack

- Python 3.12
- `http.server` from the Python standard library
- HTML
- CSS
- JavaScript
- Tailscale

## How it works

The phone opens the PC Remote page through the Windows machine's Tailscale address. Button presses send requests such as:

```text
/launch/cs2
/launch/TBOI
/launch/osu
```

The Python server handles those routes. Steam games are launched through Steam URIs:

```text
steam://rungameid/<APP_ID>
```

Non-Steam applications can be launched directly with `os.startfile()`.

## Project structure

```text
pc-remote/
├── main.py
├── static/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── images/
└── README.md
```

## Running

The project is currently configured for a specific Windows PC and Tailscale address. Local executable paths and the server host in `main.py` must be adjusted for another machine.

Start the server with:

```powershell
python main.py
```

Then open the configured Tailscale IP and port from another device connected to the same tailnet.

## Security

This project is intended for use inside a private Tailscale network. It should not be exposed directly to the public internet in its current form.

## Status

Work in progress. The current version can launch the configured Steam library and start osu! together with OpenTabletDriver from the web interface.
