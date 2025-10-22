import tkinter
import time

class Button:
    def __init__(self, master=None, text="", command=None):
        self.button = tkinter.Button(master, text=text, command=command)

    def _filter_geom_kwargs(self, kwargs):
        allowed = {"after","anchor","before","expand","fill","in","ipadx","ipady","padx","pady","side"}
        # normalize padding -> padx/pady
        if "padding" in kwargs:
            p = kwargs.pop("padding")
            if isinstance(p, (list, tuple)) and len(p) >= 2:
                kwargs.setdefault("padx", p[0])
                kwargs.setdefault("pady", p[1])
            else:
                kwargs.setdefault("padx", p)
                kwargs.setdefault("pady", p)
        # remove styling-only or unknown keys
        kwargs.pop("round", None)
        return {k: v for k, v in kwargs.items() if k in allowed}

    def pack(self, **kwargs):
        self.button.pack(**self._filter_geom_kwargs(kwargs))

    def grid(self, **kwargs):
        self.button.grid(**self._filter_geom_kwargs(kwargs))

    def place(self, **kwargs):
        self.button.place(**self._filter_geom_kwargs(kwargs))

    def config(self, **kwargs):
        self.button.config(**kwargs)

    def set_text(self, text):
        self.button.config(text=text)

    def get_text(self):
        return self.button.cget("text")

    # --- animation helpers ---
    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join(c*2 for c in hex_color)
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _color_to_rgb(self, color):
        # try hex first, otherwise use winfo_rgb
        try:
            if isinstance(color, str) and color.startswith('#'):
                return self._hex_to_rgb(color)
            r, g, b = self.button.winfo_rgb(color)
            return (r // 256, g // 256, b // 256)
        except Exception:
            return (255, 255, 255)

    def _rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))

    def animate_bg(self, to_color, duration=300, steps=None):
        """
        Animate background color from current to to_color over duration (ms).
        Returns a cancel() function to stop the animation early.
        """
        widget = self.button
        start_color = widget.cget('bg') or widget.cget('background') or '#ffffff'
        start_rgb = self._color_to_rgb(start_color)
        end_rgb = self._color_to_rgb(to_color)
        if steps is None:
            steps = max(2, int(duration / 20))

        step = 0
        cancelled = {'v': False}

        def tick():
            nonlocal step
            if cancelled['v']:
                return
            t = step / float(steps)
            cur = tuple(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * t for i in range(3))
            widget.config(bg=self._rgb_to_hex(cur))
            step += 1
            if step <= steps:
                widget.after(int(duration / steps), tick)

        widget.after(0, tick)

        def cancel():
            cancelled['v'] = True

        return cancel

    def animate_move(self, to_x, to_y, duration=300, steps=None):
        """
        Animate widget position. Works only if widget is managed by place().
        Returns a cancel() function.
        """
        widget = self.button
        try:
            current_x = widget.winfo_x()
            current_y = widget.winfo_y()
        except Exception:
            return lambda: None

        if steps is None:
            steps = max(2, int(duration / 20))

        dx = (to_x - current_x) / float(steps)
        dy = (to_y - current_y) / float(steps)
        step = 0
        cancelled = {'v': False}

        def tick():
            nonlocal step
            if cancelled['v']:
                return
            nx = int(current_x + dx * step)
            ny = int(current_y + dy * step)
            try:
                widget.place_configure(x=nx, y=ny)
            except Exception:
                pass
            step += 1
            if step <= steps:
                widget.after(int(duration / steps), tick)

        widget.after(0, tick)

        def cancel():
            cancelled['v'] = True

        return cancel

    def apply_style(self, style):
        if "bg" in style:
            self.button.config(bg=style["bg"])
        if "fg" in style:
            self.button.config(fg=style["fg"])
        if "font" in style:
            parts = style["font"].split()
            self.button.config(font=(parts[0], int(parts[1]), *parts[2:]))
        if "padding" in style:
            p = style["padding"]
            if isinstance(p, (list, tuple)) and len(p) >= 2:
                self.button.config(padx=p[0], pady=p[1])
            else:
                self.button.config(padx=p, pady=p)
        if "borderwidth" in style:
            self.button.config(borderwidth=style["borderwidth"])
        if "relief" in style:
            self.button.config(relief=style["relief"])



# compatibility: expose 'widgets' namespace so callers using module.widgets.Button work
try:
    widgets  # don't overwrite if already present
except NameError:
    class _WidgetsNamespace: ...
    widgets = _WidgetsNamespace()
    widgets.Button = Button
