# PC Remote

A small personal remote-control server for a Windows gaming PC.

PC Remote runs a lightweight Python HTTP server on Windows and exposes a mobile-friendly web interface over Tailscale. From a phone browser, the interface can launch installed Steam games and other local applications on the PC.

## Features

- Mobile-friendly game library interface
- Remote access through Tailscale
- Launch Steam games using their Steam AppID
- Read installed Steam AppIDs from `libraryfolders.vdf`
- Launch non-Steam applications from local executable paths
- Custom launch actions for osu! + OpenTabletDriver and Guitar Rig 7
- Restart into the Ubuntu machine workflow from the web interface
- Steam artwork for game cards with support for locally hosted images
- No web framework required

## Tech stack

- Python 3.12
- `http.server` from the Python standard library
- HTML
- CSS
- JavaScript
- Tailscale

## Project structure

```text
pc-remote/
├── main.py
├── server.py
├── launchers.py
├── steam.py
├── static/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── images/
├── .gitignore
└── README.md
```

### Python modules

- `main.py` — application entry point; creates and starts the HTTP server.
- `server.py` — HTTP routes, static file serving, and request handling.
- `launchers.py` — launches Steam games and local Windows applications.
- `steam.py` — reads the local Steam library and discovers installed AppIDs.

## How it works

The phone opens the PC Remote page through the Windows machine's Tailscale address. Button presses send requests to the Python HTTP server, which dispatches launch actions through `launchers.py`.

Steam games are launched through Steam URIs:

```text
steam://rungameid/<APP_ID>
```

Non-Steam applications are launched directly with `os.startfile()`.

The Steam module currently reads:

```text
D:/Steam/steamapps/libraryfolders.vdf
```

and extracts the AppIDs listed in its `apps` section. The next step is to use those IDs to build the Steam game list automatically instead of maintaining it manually.

## Running

The project is currently configured for a specific Windows PC. Local executable paths, the Steam directory, and the Tailscale host address must be adjusted for another machine.

Start the server with:

```powershell
python main.py
```

Then open the configured Tailscale IP and port from another device connected to the same tailnet.

## Security

This project is intended for use inside a private Tailscale network. It should not be exposed directly to the public internet in its current form.

## Status

Work in progress. The project has been split into separate server, launcher, and Steam modules. Installed Steam AppIDs can now be discovered from `libraryfolders.vdf`; automatic game metadata and card generation are still in development.
