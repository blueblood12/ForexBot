from typing import Union

from pandas import DataFrame

from . import Base


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

    def __repr__(self):
        return f"{self.__class__.__name__}" + '(' + ', '.join(f"{i}={{{i}}}" for i in self.__dict__.keys()).format(**self.__dict__) + ')'

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
    def __init__(self, *, data: DataFrame, candle=Candle):
        self.__data = data.iloc[::-1]
        self.Candle = candle

    def __len__(self):
        return self.__data.shape[0]

    def __contains__(self, item: Candle):
        return item.time == self[item.Index].time

    def __getitem__(self, index) -> Union[type(Candle), "Candles"]:
        if isinstance(index, slice):
            cls = self.__class__
            data = self.__data.iloc[index]
            return cls(data=data.iloc[::-1], candle=self.Candle)

        item = self.__data.iloc[index]
        return self.Candle(Index=index, **item)

    def __iter__(self):
        return (self.Candle(**row._asdict()) for row in self.__data.itertuples())

    def get_swing_high(self) -> type(Candle):
        for candle in self[1:-1]:
            if self.is_swing_high(candle):
                return candle

    def get_swing_low(self) -> type(Candle):
        for candle in self[1:-1]:
            if self.is_swing_low(candle):
                return candle

    def is_swing_high(self, candle: Candle):
        return self[candle.Index - 1].high < candle.high > self[candle.Index + 1].high

    def is_swing_low(self, candle: Candle):
        return self[candle.Index - 1].low > candle.low < self[candle.Index + 1].low

    @property
    def data(self):
        return self.__data
