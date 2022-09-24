from typing import Union

from pandas import DataFrame

from .core import Base


class Tick(Base):
    time: int
    bid: float
    ask: float
    last: float
    volume: float
    time_msc: int
    flags: int
    volume_real: float
    Index: int = 0


class Ticks:

    def __init__(self, *, data: DataFrame, turn=True):
        self.__data = data.iloc[::-1] if turn else self.data

    def __len__(self):
        return self.__data.shape[0]

    def __contains__(self, item: Tick):
        return item.time == self[item.Index].time

    def __getitem__(self, index) -> Union[Tick, "Ticks"]:
        if isinstance(index, slice):
            cls = self.__class__
            data = self.__data.iloc[index]
            return cls(data=data, turn=False)

        item = self.__data.iloc[index]
        return Tick(Index=index, **item)

    def __iter__(self):
        return (Tick(**row._asdict()) for row in self.__data.itertuples())

    @property
    def data(self):
        return self.__data
