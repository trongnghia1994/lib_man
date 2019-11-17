class BaseField:
    def __init__(self, primary_key=False, default=None):
        self.primary_key = primary_key
        self.default = default


class IntegerField(BaseField):
    pass


class TextField(BaseField):
    pass


class BooleanField(BaseField):
    pass


class DateField(BaseField):
    pass
