from tkinter import Tk


class clipboard:

    def read():
        root = Tk()
        root.withdraw()
        return(root.clipboard_get())

    def write(content):
        r = Tk()
        r.withdraw()
        r.clipboard_clear()

        r.clipboard_append(content)
        r.destroy()
