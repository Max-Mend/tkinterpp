import time
import math

class Animation:
    def __init__(self, widget, duration, update_func, on_complete=None, easing="linear"):
        self.widget = widget
        self.duration = duration
        self.update_func = update_func
        self.on_complete = on_complete
        self.start_time = None
        self.running = False
        self.easing = easing

    def start(self):
        self.start_time = time.time()
        self.running = True
        self._step()

    def _ease(self, t):
        if self.easing == "ease_in_out":
            return t * t * (3 - 2 * t)
        elif self.easing == "ease_out":
            return 1 - (1 - t) * (1 - t)
        elif self.easing == "ease_in":
            return t * t
        return t  # linear

    def _step(self):
        if not self.running:
            return

        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        eased = self._ease(progress)

        self.update_func(eased)

        if progress < 1.0:
            self.widget.after(16, self._step)
        else:
            self.running = False
            if self.on_complete:
                self.on_complete()

    def stop(self):
        self.running = False

    @staticmethod
    def animate_color(widget, from_color, to_color, duration=300, target="bg"):
        def update(progress):
            r1, g1, b1 = widget.winfo_rgb(from_color)
            r2, g2, b2 = widget.winfo_rgb(to_color)

            r = int(r1 + (r2 - r1) * progress) // 256
            g = int(g1 + (g2 - g1) * progress) // 256
            b = int(b1 + (b2 - b1) * progress) // 256

            new_color = f"#{r:02x}{g:02x}{b:02x}"
            widget.config(**{target: new_color})

        animation = Animation(widget, duration / 1000.0, update)
        animation.start()
        return animation

    @staticmethod
    def animate_move(widget, from_pos, to_pos, duration=300):
        def update(progress):
            x = int(from_pos[0] + (to_pos[0] - from_pos[0]) * progress)
            y = int(from_pos[1] + (to_pos[1] - from_pos[1]) * progress)
            widget.place(x=x, y=y)
        animation = Animation(widget, duration / 1000.0, update)
        animation.start()
        return animation

    @staticmethod
    def animate_opacity(window, from_opacity, to_opacity, duration=300):
        def update(progress):
            alpha = from_opacity + (to_opacity - from_opacity) * progress
            window.attributes("-alpha", alpha)
        animation = Animation(window, duration / 1000.0, update)
        animation.start()
        return animation

class AnimationManager:
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme

    def create(self, duration, update_func, on_complete=None, easing="linear"):
        return Animation(self.root, duration, update_func, on_complete, easing)

    # Forward convenience methods
    def animate_color(self, widget, from_color, to_color, duration=300, target="bg"):
        return Animation.animate_color(widget, from_color, to_color, duration, target)

    def animate_move(self, widget, from_pos, to_pos, duration=300):
        return Animation.animate_move(widget, from_pos, to_pos, duration)

    def animate_opacity(self, window, from_opacity, to_opacity, duration=300):
        return Animation.animate_opacity(window, from_opacity, to_opacity, duration)
