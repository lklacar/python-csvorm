class RelationType(object):
    ONE_TO_MANY = "one_to_many"
    ONE_TO_ONE = "one_to_one"


class Relation(object):
    def __init__(self, cls):
        self.cls = cls


class HasOne(Relation):
    def get(self, id):
        return self.cls.get(id=id)


class HasMany(Relation):
    def get(self, id):
        value = []
        tokens = id.split(",")

        for token in tokens:
            value += (self.cls.get(id=token.strip()))

        return value
