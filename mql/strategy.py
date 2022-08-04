import asyncio
import time
from dataclasses import dataclass
from typing import Literal
from abc import abstractmethod, ABC

import pandas_ta as ta
from pandas import DataFrame

from .constants import TimeFrame, OrderType
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
    Candle: type(Candle) = Candle
    Candles: type(Candles) = Candles

    def __init__(self, *, symbol: Symbol):
        self.symbol = symbol
        self.current = 0

    async def get_ema(self, *, time_frame: TimeFrame, period: int) -> type(Candles):
        data: DataFrame = await self.symbol.rates_from_pos(time_frame=time_frame)
        await asyncio.to_thread(data.ta.ema, length=period, append=True)
        data.rename(columns={f"EMA_{period}": 'ema'}, inplace=True)
        return self.Candles(data=data, candle=self.Candle)

    def set_params(self, **params):
        [setattr(self, key, value) for key, value in params.items()]

    @staticmethod
    async def sleep(secs: float):
        await asyncio.sleep(secs - (time.time() % secs) + 1)

    @abstractmethod
    async def trade(self):
        """trade"""
