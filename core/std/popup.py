import core

__all__ = ["Info", "Warning", "Error"]

class Info(core.render.Window):

    template = f"{core.sys.PATH}core/resource/template/info.template"

    def __init__(self, message):
        self.message = core.render.element.Text(core.Vector(38, 27), f'{message[:20]}', size=11, justify="L")#Font Was 8

    def render(self):
        self.message.render()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Info

    def press(self):
        self.window.finish()

class Warning(Info):
  template = f"{core.sys.PATH}core/resource/template/warning.template"

class Error(Info):
    template = f"{core.sys.PATH}core/resource/template/error.template"
