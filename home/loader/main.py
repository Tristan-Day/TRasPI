import core

class App(core.type.Application):
    class asset(core.asset.Pool):
        app = core.asset.Image("app-default")
        folder = core.asset.Image("folder-default")

class AppDraw(core.render.Window):

    POSITIONS = [core.Vector(x, y) for y in (13, 39) for x in (12, 39, 66, 93)]
    CURSOR = (core.Vector(-2, -1), App.asset.app.size()+core.Vector(1, 0))

    def __init__(self, tree=core.sys.load.tree["programs"], name="/"):
        super().__init__()
        self.apps = [self.__file(v) if isinstance(v, str) else self.__folder(tree[k], f"{name}{k}/") for k,v in tree.items()]
        self.icon_elm = [core.element.Image(self.POSITIONS[index % len(self.POSITIONS)], App.asset.app if isinstance(value, str) else App.asset.folder, just_w="L") for index, value in enumerate(tree.values())]
        self.index = 0
        self._render_elm = set()
        self.title = core.element.Text(core.Vector(1, 5), name, justify="L")
        self.cursor = core.element.Rectangle(*self.CURSOR)

        self.update()

    def __file(self, path):
        async def _file():
            prog = core.sys.load.app(path, full=True)
            core.Interface.program(prog)
        return _file
    def __folder(self, path, name):
        async def _folder():
            await self.__class__(path, name)
        return _folder

    def render(self):
        for elm in (*self._render_elm, self.cursor, self.title):
            core.Interface.render(elm)

    def update(self):
        index = self.index // len(self.POSITIONS)
        self._render_elm = {elm for elm in self.icon_elm[index:min(index+len(self.POSITIONS), len(self.icon_elm))]}
        offset = self.POSITIONS[self.index % len(self.POSITIONS)]
        self.cursor.pos1 = self.CURSOR[0] + offset
        self.cursor.pos2 = self.CURSOR[1] + offset

    async def run(self):
        app = self.apps[self.index]
        await app()

class Handle(core.input.Handler):

    window = AppDraw

    class press:
        async def right(null, window: AppDraw):
            window.index = (window.index + 1) % len(window.apps)
            window.update()
        async def left(null, window: AppDraw):
            window.index = (window.index - 1) % len(window.apps)
            window.update()

        async def up(null, window: AppDraw):
            window.finish()

        async def centre(null, window: AppDraw):
            await window.run()


App.window = AppDraw
main = App