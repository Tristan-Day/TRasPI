import core

class App(core.type.Application):
    name = "Dungeon Runner"

    class var(core.type.Config):
        pass

    class const(core.type.Constant):
        pass

    class asset(core.type.Pool):
        ts_template = core.asset.Template("ts_template")
        ts_keyboard = core.asset.Image("fs_keyboard")
        ts_title = core.asset.Image("ts_title")
        ts_cursor = core.asset.Image("ts_cursor")

main = App