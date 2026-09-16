from . import config
import tkinter as tk

from tkinter import filedialog


def select_executable() -> str | None:
    root = tk.Tk()
    
    root.withdraw()
    
    path = filedialog.askopenfilename()
    return path

def run_setup():
    while True:
        path = select_executable()

        if not path:
            return

        name = input("App Name: ")
        add_launch_before = input("Anything needs to be launched before?[Y/n]: ")
        launch_before = None
        if add_launch_before.lower() in ("y", "yes", ""):
            launch_before = list(filedialog.askopenfilenames())

        config.add_standalone(name, path, launch_before)
        add_another = input("Add another app? [y/N]: ")
        if add_another.lower() not in ("y", "yes"):
            break
    

run_setup()