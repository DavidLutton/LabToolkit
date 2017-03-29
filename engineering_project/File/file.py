import tkinter as tk
from tkinter import filedialog


def fileopen(title="Open", filetypes=(("All files", "*.*"), )):
    root = tk.Tk()
    root.withdraw()
    return(filedialog.askopenfilename(title=title, filetypes=filetypes))
    # ("Template files", "*.tplate"), ("HTML files", "*.html;*.htm"),
    # initialdir = "E:/Images",


def filesave(title="Save", filetypes=(("All files", "*.*"), )):
    root = tk.Tk()
    root.withdraw()
    return(filedialog.asksaveasfilename(title=title, filetypes=filetypes))


def opendir():
    pass
    # filedialog.askdirectory
