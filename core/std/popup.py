import core

__all__ = ["Info", "Warning", "Error"]

class Info(core.render.Window):

    template = core.asset.Template("std::info", path="info.template")

    def __init__(self, message):
        self.message = core.element.Text(core.Vector(38, 27), f'{message[:20]}', size=11, justify="L")#Font Was 8

    def render(self):
        self.message.render()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Info

    def press(self):
        self.window.finish()

class Warning(Info):
  template = core.asset.Template("std::warning", path="warning.template")

class Error(Info):
    template = core.asset.Template("std::error", path="error.template")

import core.render.screen

@core.render.Window.focus
def event_error_callback(error):
    print("TRYING TO YIELD")
    yield Error("EVENT")

core.render.screen.Screen().callback = event_error_callback