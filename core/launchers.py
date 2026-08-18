import os
import subprocess

from pathlib import Path


OTD_PATH = Path(
    "C:/Users/timbr/Desktop/OTD/OpenTabletDriver.UX.Wpf.exe"
)
OSU_PATH = Path("D:/OSUSTBL/osu!.exe")
GR7_PATH = Path(
    "C:/Native Instruments/Guitar Rig 7/Guitar Rig 7.exe"
)


def launch_osu():
    os.startfile(OTD_PATH)
    os.startfile(OSU_PATH)


def launch_gr7():
    os.startfile(GR7_PATH)


def launch_ubuntu():
    subprocess.run(
        ["shutdown", "/r", "/t", "0"],
        cwd=None,
        check=True,
    )


def launch_app(app_id: int):
    os.startfile(f"steam://rungameid/{app_id}")
