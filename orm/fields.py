class BaseField:
    def __init__(self, primary_key=False, default=None, column_name=None):
        self.primary_key = primary_key
        self.default = default
        self.column_name = column_name


class IntegerField(BaseField):
    pass


class TextField(BaseField):
    pass


class BooleanField(BaseField):
    pass


class DateField(BaseField):
    pass
