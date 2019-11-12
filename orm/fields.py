class BaseField:
    def __init__(self, primary_key=False, default=None):
        self.primary_key = primary_key
        self.default = default


class IntergerField(BaseField):
    def __init__(self):
        BaseField.__init__(self)


class TextField(BaseField):
    def __init__(self):
        BaseField.__init__(self)


class BooleanField(BaseField):
    def __init__(self):
        BaseField.__init__(self)
