from apistar.types import Type


class BaseType(Type):
    def __setstate__(self, d):
        object.__setattr__(self, '__dict__', d)
