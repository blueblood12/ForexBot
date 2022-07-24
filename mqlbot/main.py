from typing import Iterable, Mapping


class Base:
    def __init__(self, **kwargs):
        self.set_attributes(**kwargs)

    def set_attributes(self, **kwargs):
        [setattr(self, i, j) for i, j in kwargs.items()]

    @property
    def dict(self):
        return self.__dict__

    @dict.setter
    def dict(self, value: Mapping | Iterable[Iterable]):
        self.dict.update(value)
