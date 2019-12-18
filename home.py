import core
import time

class Mainwindow(core.render.Window):

    def __init__(self):
        # Elements
        self.template = f"{core.sys.PATH}core/resource/template/home.template"
        self.title1 = core.render.element.Text(core.Vector(3, 5), "TRasPi OS", colour=0, justify="L") #Could be part of template
        self.title2 = core.render.element.Text(core.Vector(126, 5), time.strftime('%I:%M %r'), colour=0, justify="R")
        self.bttn1 = core.render.element.Text(core.Vector(64, 10), "Run Program")
        self.bttn2 = core.render.element.Text(core.Vector(64, 20), "Load Program")
        self.bttn3 = core.render.element.Text(core.Vector(64, 30), "System Settings")
        self.bttn4 = core.render.element.Text(core.Vector(64, 40), "Power Options")
        # Variables
        self.index = 0
        self.functions = {0: core.loader.run, 1: core.render.load, 2: core.sys.configurator, 3: core.sys.powermenu} #Needs to be ajusted if name changes

    def up(self):
        if self.index > 0:
            self.index -=1 #Needs to reposiiton 

    def down(self):
        if self.index < len(self.functions):
            self.index +=1

    def select(self):
        pass


class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Mainwindow

    def press(self):
        self.window.select()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = Mainwindow

    def press(self):
        self.window.up()

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = Mainwindow

    def press(self):
        self.window.down()