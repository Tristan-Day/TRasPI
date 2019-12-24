from core.render.single import Singleton
try:
    from gfxhat import touch
except ModuleNotFoundError:
    from core.hardware.dummy import touch

__all__ = ["Screen"]

class Screen(metaclass=Singleton):

    def __init__(self):
        self.active = None
        self.callstack = []

        touch.enable_repeat(True)
        touch.set_repeat_rate(50)

    def template(self):
        return self.active.template

    def call_focus(self, generator, window):
        self.callstack.append((window, generator))

    def call_lost(self) -> tuple:
        return self.callstack.pop()

    def show(self, window):
        self.active = window
        self.bind_handles()

    def bind_handles(self):
        for key, handler in enumerate(self.active._handles):
            if handler is None:
                touch.on(key, lambda c, e: None)
                continue
            def wrap(handler):
                def handle(ch, event):
                    try:
                        func = getattr(handler(self.active), event)
                    except AttributeError:    return
                    result = func()
                    if type(result).__name__ == "generator":
                        return self.active._handle_focus(None, result)

                return handle
            touch.on(key, wrap(handler))

    def render(self):
        self.active.render()

    def pause(self):
        pass

    def resume(self):
        pass

def render():
    Screen().render()
