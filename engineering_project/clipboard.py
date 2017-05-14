from tkinter import Tk


class clipboard(object):
    """Retrieve and set content with clipboard."""

    def read():
        """Get a copy of the contents of the clipboard.

        :returns: copy of the clipboard
        """
        root = Tk()
        root.withdraw()
        return(root.clipboard_get())

    def write(content):
        """Write content ot the clipboard.

        :param content: to be written to clipboard
        """
        r = Tk()
        r.withdraw()
        r.clipboard_clear()

        r.clipboard_append(content)
        r.destroy()
