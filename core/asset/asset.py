class Asset(type):

    _instances = {}

    def __new__(cls, name_, bases, dct):
        @property
        def name(self):
            return self._name
        @property
        def path(self):
            return self._path
        dct["name"] = name
        dct["path"] = path

        if "__init__" in dct:
            def wrap(func):
                def __init__(self, name, path, *args, **kwargs):
                    self._name = name
                    self._path = path
                    func(self, *args, **kwargs)
                return __init__
            dct["__init__"] = wrap(dct["__init__"])
        return super().__new__(cls, name_, bases, dct)

    def __init__(cls, name, bases, dct):
        cls._instances[cls] = {}
        return super().__init__(name, bases, dct)

    def __call__(cls, name: str, *args, path=None, new=False, **kwargs):
        # print(cls, name, args, path, new, kwargs)
        if path is None:
            if new:
                path = cls._instances[cls][name]._path
                name += "_new"
                self = super().__call__(name, path, *args, **kwargs)
                return self
            else:
                return cls._instances[cls][name]
        else:
            self = super().__call__(name, path, *args, **kwargs)
            cls._instances[cls][name] = self
            return self