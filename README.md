# TRasPi Operating System
Raspberry Pi code

For a list of future changes see TODO.odt 

# Creating A Program

## Main

A `Program` is a folder containing a file *`main.py`* as its entry point.
This file must then provide an attribute named *`main`* that is a subclass of [`core.type.Application`](#coretypeapplication).

## Resource

A program will have a *`resource`* folder (not mandatory but it will be generated by core).
This folder is the directory in which assets will be searched for following the [type structure](#coreasset).
This also holds the folder containing the [`var`](#coretypeapplicationvar) data which can be deleted if it needs to be cleared manually.

# Referance

### `core.type.Application`
*class* `core.type.Application`

An `Application` is used to help define the entry point for a program.
You should never instantiate this class or any subclasses directly.
Futhermore, you should not use this instance of the class as your `Program`s entry point.

#### `core.type.Application.window`
*Type* class [`core.render.Window`](#corerenderwindow)

`window` will be the first [`Window`](#corerenderwindow) in the window stack when the program is launched and will be instantiated by core.
For this reason it should take no extra arguments other than self or optional ones.
It must be set otherwise it will not be able to load.

#### `core.type.Application.name`
*Type* `str`

The `name` attribute is used as the display name for your program and the folder name will never be used.
It should not be changed after the program has been loaded as it may result in undefined behaviour.

#### `core.type.Application.interval`
interval(func: callable, delay: float=1, repeat: int=-1) -> [`core.interface.interval`](#coreinterfaceinterval)

This function will create an [`interval`](#coreinterfaceinterval).
These will be executed according to the `delay` and `repeat` while the entire program has got focus.
Once the program loses the focus it will no longer be executed and paused until it regains it.

#### `core.type.Application.open`
*async* open()

This will be called upon the program being opened for the first time.
If this function fails, the program will still continue to execute which might cause problems in your `Program`.

#### `core.type.Application.close`
*async* close()

This will be called upon the program being closed.
Exceptions thrown will be ignored.

#### `core.type.Application.show`
*async* show()

This will be called upon the program being shown and given focus. This is be after any calls to open.
If this function fails, the program will still continue to execute which might cause problems in your `Program`.

#### `core.type.Application.var`
*Type* class [`core.type.Config`](#coretypeconfig)

The attributes of `var` will be the default values.
All values inside of `var` will be saved to a file during the `close` event.
This is done using [`pickle`](https://docs.python.org/3/library/pickle.html) so all attributes must be picklable to be able to be stored.
When the program is sent the `open` event, it will read the data stored in the file and update the values or `var` to match.
If no file is found then it will use the default values.
Because the loading of the data happens during the `open` event, if any `var` values are used at the module level during importing, then it will be the default values, and `var` will be overriden by the file even if any attributes have been changed beforehand.

#### `core.type.Application.const`
*Type* class [`core.type.Constant`](#coretypeconstant)

A helper class to help store constants across the program.

#### `core.type.Application.asset`
*Type* class [`core.type.Pool`](#coretypepool)

A helper class to help store assets across the program.

### `core.type.Config`
*class* `core.type.Config`

Stores all vars in a file at close and reads them on open. To be subclassed
Callbacks for when a value changes
\# TODO: Explain implmentation

### `core.type.Constant`
*class* `core.type.Constant`

Values can not be changed
\# TODO: Explain implmentation

### `core.type.Pool`
*class* `core.type.Pool`

Just stores the assets
\# TODO: Explain implmentation

### `core.render.Window`
*class* `core.render.Window`

The `Window` is used to contain [`elements`](#coreelement) and display them.

#### `core.render.Window.render`
render()

Override to provide functionality.
`render` is called every frame and is used to sumbit [`elements`](#coreelement) to the screen.

#### `core.render.Window.show`
*async* show()

Override to provide functionality.
This is called during the `show` event.
It will be called every time the `Window` gets [`focus`](#corerenderWindowfocus).

#### `core.render.Window.hide`
*async* hide()

Override to provide functionallity.
This is called during the `hide` event.
It will be called every time the `Window` loses [`focus`](#corerenderWindowfocus).

#### `core.render.Window.focus`
*async* focus()

This will set the current active window of the renderer to this `Window`.
This will hang execution in the caller until this `Window` makes a call to `Window.finish`.
`await Window.focus()` is synonymous to `await Window`. It will [`hide`](#corerenderWindowhide) the current active `Window`.
It will return the value of `Window.finish` argument.

#### `core.render.Window.finish`
*async* finish(value: Any=None)

Returns focus to the previous `Window` in the stack.
The return value will be sent to the return value of `Window.focus`.

# Example

## Example Program

```python
import core

class App(core.type.Application):
    name = "My Program" # Display Name

    class var(core.type.Config):
        # These can be edited by the program so the new values will be saved on file and reloaded later
        x = 4
        y = 7

    class const(core.type.Constant):
        alice = "Alice the First" # Can never be changed
        bob = "Bob the Second" # Can never be changed

    class asset(core.type.Pool):
        myfont = core.asset.Font("filename", 11)

App.window = MyWindow
main = App
```

## Eaxmple Window

```python
import core

class MyWindow(core.render.Window):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.count = 0
        self.rate = 1

        self.text = core.element.Text(
            core.Vector(core.sys.const.width // 2, core.sys.const.height // 2), # Position of the Element
            "Counter:",
        )

        self.counter = core.element.Text(
            core.Vector(core.sys.const.width // 2, core.sys.const.height // 2 + 20), # Position of the Element
            self.count,
        )

        def render(self):
        # Called every frame
        # Render the elements
        core.interface.render(self.text)
        core.interface.render(self.counter)

        def refresh(self):
            self.count += self.rate
            self.counter.text = self.count

        async def show(self):
            # Called when the window is shown and given focus
            self.count = 0
            self.counter.text = self.count
```

## Example Handler

```python
import core

class MyHandler(core.input.Handler):

    window = MyWindow # The Window class that this Handler is attached to

    class press: # The `press` event

        async def up(self, window: MyWindow):
            # `up` refers to the button
            # `window` will be the window instance that is linked to the handler
            window.rate += 1

        async def down(self, window: MyWindow):
            window.rate -= 1

        async def centre(self, window: MyWindow):
            self.count = await AnotherWindow(self.count)

        async def left(self, window: MyWindow):
            self.finish(self.count)
```
