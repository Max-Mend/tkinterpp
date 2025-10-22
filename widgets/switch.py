import tkinter
import time

class Switch:
    def __init__(self, master=None, on_text="On", off_text="Off", command=None):
        self.var = tkinter.BooleanVar()
        self.switch = tkinter.Checkbutton(
            master,
            text=off_text,
            variable=self.var,
            command=self._toggle_command(command, on_text, off_text)
        )
        self.on_text = on_text
        self.off_text = off_text

    def _toggle_command(self, command, on_text, off_text):
        def toggle():
            if self.var.get():
                self.switch.config(text=on_text)
            else:
                self.switch.config(text=off_text)
            if command:
                command()
        return toggle

    def _filter_geom_kwargs(self, kwargs):
        allowed = {"after","anchor","before","expand","fill","in","ipadx","ipady","padx","pady","side"}
        if "padding" in kwargs:
            p = kwargs.pop("padding")
            if isinstance(p, (list, tuple)) and len(p) >= 2:
                kwargs.setdefault("padx", p[0])
                kwargs.setdefault("pady", p[1])
            else:
                kwargs.setdefault("padx", p)
                kwargs.setdefault("pady", p)
        kwargs.pop("round", None)
        return {k: v for k, v in kwargs.items() if k in allowed}

    def pack(self, **kwargs):
        self.switch.pack(**self._filter_geom_kwargs(kwargs))

    def grid(self, **kwargs):
        self.switch.grid(**self._filter_geom_kwargs(kwargs))

    def place(self, **kwargs):
        self.switch.place(**self._filter_geom_kwargs(kwargs))

    def config(self, **kwargs):
        self.switch.config(**kwargs)

    def is_on(self):
        return self.var.get()

    def set_on(self, value):
        self.var.set(value)
        if value:
            self.switch.config(text=self.on_text)
        else:
            self.switch.config(text=self.off_text)

    # --- animation helpers ---
    def _color_to_rgb(self, color):
        try:
            if isinstance(color, str) and color.startswith('#'):
                hex_color = color.lstrip('#')
                if len(hex_color) == 3:
                    hex_color = ''.join(c*2 for c in hex_color)
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            r, g, b = self.switch.winfo_rgb(color)
            return (r // 256, g // 256, b // 256)
        except Exception:
            return (255, 255, 255)

    def _rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))

    def animate_bg(self, to_color, duration=300, steps=None):
        widget = self.switch
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
        widget = self.switch
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
            self.switch.config(bg=style["bg"])
        if "fg" in style:
            self.switch.config(fg=style["fg"])
        if "font" in style:
            parts = style["font"].split()
            self.switch.config(font=(parts[0], int(parts[1]), *parts[2:]))
        if "padding" in style:
            p = style["padding"]
            if isinstance(p, (list, tuple)) and len(p) >= 2:
                self.switch.config(padx=p[0], pady=p[1])
            else:
                self.switch.config(padx=p, pady=p)
        if "borderwidth" in style:
            self.switch.config(borderwidth=style["borderwidth"])
        if "relief" in style:
            self.switch.config(relief=style["relief"])

# compatibility: expose 'widgets' namespace so callers using module.widgets.Switch work
try:
    widgets
except NameError:
    class _WidgetsNamespace: ...
    widgets = _WidgetsNamespace()
    widgets.Switch = Switch
