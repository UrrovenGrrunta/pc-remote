# PC Remote

A small personal remote-control server for a Windows gaming PC.

PC Remote runs a lightweight Python HTTP server on Windows and exposes a mobile-friendly web interface over Tailscale. From a phone browser, the interface can launch installed Steam games and other local applications on the PC.

## Features

- Mobile-friendly game library interface
- Remote access through Tailscale
- Dynamic Steam game discovery from local `appmanifest_*.acf` files
- Steam metadata and artwork loaded from the Steam Store API
- Launch Steam games using their Steam AppID
- Launch non-Steam applications from local executable paths
- Custom launch actions for osu! + OpenTabletDriver and Guitar Rig 7
- Restart into the Ubuntu machine workflow from the web interface
- Experimental Hydra library investigation
- No web framework required

## Tech stack

- Python 3.12
- `http.server` from the Python standard library
- HTML
- CSS
- JavaScript
- Node.js for experimental Hydra/LevelDB tooling
- Tailscale

## Project structure

```text
pc-remote/
├── main.py
├── core/
│   ├── config.py
│   ├── launchers.py
│   └── server.py
├── providers/
│   ├── steam.py
│   ├── hydra.py
│   └── hydra_reader.js
├── documents/
│   ├── UGPEP.md
│   └── UGPEP_RU.md
├── static/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── images/
├── package.json
├── package-lock.json
├── .gitignore
└── README.md
```

## Modules

- `main.py` — application entry point.
- `core/server.py` — HTTP routes, static file serving, and request handling.
- `core/launchers.py` — launches Steam games and local Windows applications.
- `core/config.py` — reserved for project configuration work.
- `providers/steam.py` — discovers installed Steam AppIDs from manifest filenames and retrieves game metadata from the Steam Store API.
- `providers/hydra.py` — experimental Hydra database/SSTable investigation.
- `providers/hydra_reader.js` — experimental Node.js LevelDB reader used during Hydra research.

## Documentation

The repository contains the semi-official **UGPEP — UrrovenGrrunta Python Enhancement Proposal**, a project-level Python style guide built on top of PEP 8 with additional conventions for readability, import layout, experimental code, development history, bilingual graveyard records, and Paranormal-Driven Development.

- `documents/UGPEP.md` — English version.
- `documents/UGPEP_RU.md` — Russian version.

## How it works

The phone opens the PC Remote page through the Windows machine's Tailscale address. The frontend requests the current Steam application list from the Python HTTP server and dynamically builds game cards from the returned metadata.

Steam games are launched through Steam URIs:

```text
steam://rungameid/<APP_ID>
```

Non-Steam applications can be launched directly with `os.startfile()`.

Installed Steam applications are discovered from files matching:

```text
appmanifest_*.acf
```

inside the configured Steam `steamapps` directory. The AppID is extracted from each manifest filename, while the Steam Store API supplies display names and artwork.

## Hydra support

Hydra support is currently experimental. The investigation has progressed into direct parsing of LevelDB SSTable data after the local Hydra database was found to contain corrupted blocks that could not be read reliably through the normal LevelDB API.

This code is research-stage and should not yet be treated as production functionality.

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

Work in progress. Steam discovery, metadata loading, dynamic web cards, and AppID-based launching are functional. Hydra integration is under active investigation.
