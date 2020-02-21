import core
import json
import time

default = "default"
timeout = True


class Main(core.render.Window):

    def __init__(self):
        self.timer = 0
        self.timeout = 0
        self.data = self.load(default)
        core.asset.Template(
            "template", path=f"{core.sys.PATH}programs/Toolbox/Clock/package/{default}/template.template")
        core.hardware.Backlight.gradient([int(val) for val in self.data["backlight"][0]], saturation=int(
            self.data["backlight"][1]), value=int(self.data["backlight"][2]))
        self.elements = [(core.element.Text(core.Vector(int(element["pos"][0]), int(element["pos"][1])), text="LDR", font=element["font"], size=int(
            element["size"]), colour=int(element["colour"]), justify=element["justify"]), element["format"]) for element in self.data["elements"]]
        print(([int(val) for val in self.data["backlight"][0]], int(
            self.data["backlight"][1]), int(self.data["backlight"][2])))

    def active(self):
        print(([int(val) for val in self.data["backlight"][0]], int(
            self.data["backlight"][1]), int(self.data["backlight"][2])))
        core.hardware.Backlight.gradient([int(val) for val in self.data["backlight"][0]], saturation=int(
            self.data["backlight"][1]), value=int(self.data["backlight"][2]))
        self.timeout = 0

    def inactive(self):
        core.hardware.Backlight.gradient([int(val) for val in self.data["backlight"][0]], saturation=int(
            self.data["backlight"][1]), value=0.1)

    def render(self):
        for element in self.elements:
            element[0].text(time.strftime(element[1]))
            element[0].render()
        if time.time() - self.timer > 1 and 60 >= self.timeout:
            self.timeout += 1
            self.timer = time.time()
            if self.timeout == 60:
                self.inactive()
        print(self.timeout)

    def load(self, package):
        try: 
            with open(f"{core.sys.PATH}programs/Toolbox/Clock/package/{package}/main.cfg", 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            self.errorHandle("No File")
        except json.JSONDecodeError:
            self.errorHandle("JSON Error")

    @core.render.Window.focus
    def errorHandle(self, string):
        print(string)
        yield core.std.Error(string)
        self.finish()


class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = Main

    def press(self):
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = Main

    def press(self):
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = Main

    def press(self):
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = Main

    def press(self):
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Main

    def press(self):
        self.window.active()


class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Main

    def press(self):
        self.window.finish()


main = Main()
