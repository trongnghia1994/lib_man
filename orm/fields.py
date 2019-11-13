class BaseField:
    def __init__(self, primary_key=False, default=None):
        self.primary_key = primary_key
        self.default = default


class IntergerField(BaseField):
    pass


class TextField(BaseField):
    pass


class BooleanField(BaseField):
    pass
