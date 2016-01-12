class Field(object):
    def __init__(self, value=None):
        self.value = value

    def set(self, value):
        self.value = value

    def get(self):
        return self.value


class IntegerField(Field):
    pass


class StringField(Field):
    pass


class DateTimeField(Field):
    pass
