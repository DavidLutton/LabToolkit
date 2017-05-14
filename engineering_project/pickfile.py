import tkinter as tk
from tkinter import filedialog


def pickfileopen(title="Open", filetypes=(("All files", "*.*"), )):
    """Pick a file, return the filepath."""
    root = tk.Tk()
    root.withdraw()
    return(filedialog.askopenfilename(title=title, filetypes=filetypes))
    # ("Template files", "*.tplate"), ("HTML files", "*.html;*.htm"),
    # initialdir = "E:/Images",


def pickfilesave(title="Save", filetypes=(("All files", "*.*"), )):
    """Pick a location/name to save a file."""
    root = tk.Tk()
    root.withdraw()
    return(filedialog.asksaveasfilename(title=title, filetypes=filetypes))


def pickopendir(*, args):
    """Pick a directory."""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(args)
