class RelationType(object):
    ONE_TO_MANY = "one_to_many"
    ONE_TO_ONE = "one_to_one"


class Relation(object):
    def __init__(self, cls):
        self.cls = cls

    def get(self, **kwargs):
        pass

    def set(self, **kwargs):
        pass


class HasOne(Relation):
    def get(self, **kwargs):
        id = kwargs['id']
        return self.cls.get(id=id)[0]


class HasMany(Relation):
    def get(self, **kwargs):
        id = kwargs['id']

        value = []
        tokens = id.split(",")

        for token in tokens:
            value += (self.cls.get(id=token.strip()))

        return value
