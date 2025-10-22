import tkinter

from .ttkpp import ttkpp
from .widget import Widget
from .animation import Animation, AnimationManager

class Tkpp:
    def __init__(self, master=None, css="default.css"):
        self.tkinterpp = tkinter.Tk() if master is None else master
        self.tkinterpp.withdraw()
        self.tkinterpp.title("tkinter++")

        self.width = self.tkinterpp.winfo_screenwidth()
        self.height = self.tkinterpp.winfo_screenheight()

        self.theme = ttkpp(root=self.tkinterpp)

        self.widget = Widget(master=self.tkinterpp)
        # Use AnimationManager which accepts (root, theme)
        self.animation = AnimationManager(self.tkinterpp, self.theme)

    def geometry(self, width, height):
        self.tkinterpp.geometry(f"{width}x{height}")

    def title(self, title):
        self.tkinterpp.title(title)

    def mainloop(self):
        self.tkinterpp.deiconify()
        self.tkinterpp.mainloop()
