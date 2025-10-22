
class Widget:
    def __init__(self, master=None):
        self.master = master
        self.widget = None

    def pack(self, **kwargs):
        if self.widget:
            self.widget.pack(**kwargs)

    def grid(self, **kwargs):
        if self.widget:
            self.widget.grid(**kwargs)

    def place(self, **kwargs):
        if self.widget:
            self.widget.place(**kwargs)

    def config(self, **kwargs):
        if self.widget:
            self.widget.config(**kwargs)