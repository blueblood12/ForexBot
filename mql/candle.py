from typing import Union, Type

from pandas import DataFrame

from .core import Base


class Candle(Base):
    Index: int
    time: int
    open: float
    high: float
    low: float
    close: float
    tick_volume: float
    real_volume: float
    spread: float
    ema: float

    def __lt__(self, other: 'Candle'):
        return self.Index < other.Index

    def __hash__(self):
        return hash(self.time)

    @property
    def mid(self):
        return (self.open + self.close) / 2

    def is_bullish(self):
        return self.close > self.open

    def is_bearish(self):
        return self.open > self.close

    def is_hanging_man(self, ratio=1.5):
        return max((self.open - self.low), (self.high - self.close)) / (self.close - self.open) >= ratio

    def is_bullish_hammer(self, ratio=1.5):
        return max((self.close - self.low), (self.high - self.open)) / (self.open - self.close) >= ratio


class Candles:
    def __init__(self, *, data: DataFrame, candle: Type[Candle] = Candle, turn=True):
        self._data = data.iloc[::-1] if turn else data
        self.Candle = candle

    def __len__(self):
        return self._data.shape[0]

    def __contains__(self, item: Candle):
        return item.time == self[item.Index].time

    def __getitem__(self, index) -> Union[type(Candle), "Candles"]:
        if isinstance(index, slice):
            cls = self.__class__
            data = self._data.iloc[index]
            return cls(data=data, candle=self.Candle, turn=False)

        item = self._data.iloc[index]
        return self.Candle(Index=index, **item)

    def __iter__(self):
        return (self.Candle(**row._asdict()) for row in self._data.itertuples())

    @property
    def data(self):
        return self._data
