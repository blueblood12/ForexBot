import asyncio
import time
from dataclasses import dataclass
from typing import Literal, Type
from abc import ABC, abstractmethod

import pandas_ta as ta
from pandas import DataFrame

from .core.constants import TimeFrame, OrderType
from .candle import Candles, Candle
from .symbol import Symbol


@dataclass
class Entry:
    time: float = 0
    trend: Literal["notrend", "uptrend", "downtrend"] = "notrend"
    current: float = 0
    new: bool = True
    type: OrderType | None = None
    points: float = 0


class Strategy(ABC):
    Candle: Type[Candle] = Candle
    Candles: Type[Candles] = Candles
    name:  str = ""

    def __init__(self, *, symbol: Symbol, **kwargs):
        self.symbol = symbol
        self.current = 0
        self.name = self.name or self.__class__.__name__

    def __repr__(self):
        return f"{self.name}({self.symbol!r})"

    async def get_ema(self, *, time_frame: TimeFrame, period: int) -> type(Candles):
        data: DataFrame = await self.symbol.rates_from_pos(time_frame=time_frame)
        await asyncio.to_thread(data.ta.ema, length=period, append=True)
        data.rename(columns={f"EMA_{period}": 'ema'}, inplace=True)
        return self.Candles(data=data, candle=self.Candle)

    @property
    @abstractmethod
    def parameters(self) -> dict:
        """return parameters as dict """

    @parameters.setter
    @abstractmethod
    def parameters(self, params: dict):
        """return parameters as dict """

    @staticmethod
    async def sleep(secs: float):
        await asyncio.sleep(secs - (time.time() % secs) + 1)

    @abstractmethod
    async def trade(self):
        """trade"""
