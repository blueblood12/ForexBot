from typing import Union

from pandas import DataFrame

from mqlbot import Base


class Candle(Base):
    time: int
    open: float
    high: float
    low: float
    close: float
    tick_volume: float
    real_volume: float
    spread: float
    ema: float

    @property
    def mid(self):
        return (self.open + self.close) / 2

    def is_bullish(self):
        return self.close > self.open

    def is_bearish(self):
        return self.open > self.close

    def is_hanging_man(self, ratio=1.5):
        return max((self.open-self.low), (self.high-self.close)) / (self.close-self.open) >= ratio

    def is_bullish_hammer(self, ratio=1.5):
        return max((self.close-self.low), (self.high-self.open)) / (self.open-self.close) >= ratio

    def ema_crossover(self):
        # return self.open > self.ema > self.close
        return self.open < self.ema < self.close

    def ema_cross_under(self):
        # return self.open < self.ema < self.close
        return self.open > self.ema > self.close


class Candles:
    def __init__(self, *, data: DataFrame):
        self.__data = data

    def __len__(self):
        return self.__data.shape[0]

    def __getitem__(self, index) -> Union[Candle, "Candles"]:
        if isinstance(index, slice):
            cls = self.__class__
            data = self.__data.loc[index]
            return cls(data=data)

        item = self.__data.iloc[index]
        return Candle(**item)

    def __iter__(self):
        return (Candle(**row._asdict()) for row in self.__data.itertuples(index=False))

    @property
    def data(self):
        return self.__data
