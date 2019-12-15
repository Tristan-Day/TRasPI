import core

__all__ = ["Query"]

class Query(core.render.Window):

    template = f"{core.sys.PATH}core/asset/template/query.template"

    def __init__(self, message, title, allow_cancel=None):
        self.message = core.render.element.Text(core.Vector(64, 16), message) #FONT: 10
        self.selection = True
        if allow_cancel is not None:
            self.cancel = core.render.element.Text(core.Vector(64, 16), "To Cancel Press 'Return'", size=11) #FONT: 8
        else:
            self.cancel = None

    def render(self):
        self.message.render()
        if self.cancel is not None:
            self.cancel.render()

    def select_left():
        self.selection = True

    def select_right():
        self.selection = False

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = Query

    def press(self):
        self.window.select_left()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = Query

    def press(self):
        self.window.select_right()


class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Query

    def press(self):
        self.window.finish(self.selection#NOT RITE)

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Query

    def press(self):
        self.window.finish()
