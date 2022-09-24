from typing import Iterable, Mapping, Any

import MetaTrader5


class Base:
    def __init__(self, **kwargs):
        self.set_attributes(**kwargs)

    def __repr__(self):
        values = ', '.join(f"{name}={value!r}" for name, value in self.__dict__.items())
        return f"{self.__class__.__name__}({values})"

    def set_attributes(self, **kwargs):
        [setattr(self, i, j) for i, j in kwargs.items()]

    def get_dict(self, exclude: set = None, include: set = None) -> dict:
        exclude, include = exclude or set(), include or set()
        filter = include or set(self.dict.keys()).difference(exclude)
        return {key: value for key, value in self.dict.items() if key in filter}

    @property
    def class_vars(self):
        return {key: value for key, value in self.__class__.__dict__.items() if not (key.startswith("__") and key.endswith("__"))}

    @property
    def dict(self):
        return {key: value for key, value in self.__dict__.items() | self.class_vars.items() if key not in self.Config.exclude}

    @dict.setter
    def dict(self, value: Mapping | Iterable[Iterable]):
        self.dict.update(value)

    class Config:
        exclude = {'retcode', 'comment', 'request', 'mt5', 'retcode_external', "Config", "request_id"}


class BaseMeta(type):
    def __new__(mcs, cls_name, bases, cls_dict):
        platform = cls_dict.get('platform')
        defaults = {} if platform is None else platform.__dict__
        defaults = {f'_{key}': value for key, value in defaults.items() if not key.startswith('_')}
        cls_dict |= defaults
        return super().__new__(mcs, cls_name, bases, cls_dict)


class Platform(metaclass=BaseMeta):
    platform: MetaTrader5 = MetaTrader5
