import asyncio
import time
from dataclasses import dataclass
from typing import Literal
from abc import abstractmethod, ABC

import pandas_ta as ta

from mqltrader import MqlTrader
from constants import TimeFrame, OrderType
from candle import Candles
from symbol import Symbol, Synthetic


@dataclass
class Entry:
    time: float = 0
    trend: Literal["notrend", "uptrend", "downtrend"] = "notrend"
    current: float = 0
    new: bool = True
    type: OrderType | None = None


class Strategy(ABC):
    def __init__(self, *, symbol: str, trader: MqlTrader):
        self.trader = trader
        self.symbol = Symbol(name=symbol) if self.trader.account.market == 'financial' else Synthetic(name=symbol)
        self.current = 0

    async def get_ema(self, *, time_frame: TimeFrame, period: int) -> Candles:
        data = await self.symbol.rates_from_pos(time_frame=time_frame)
        await asyncio.to_thread(data.ta.ema, length=period, append=True)
        name = f"EMA_{period}"
        data = data.rename(columns={name: 'ema'})
        return Candles(data=data)

    @staticmethod
    async def sleep(secs: float):
        await asyncio.sleep(secs - (time.time() % secs) + 1)

    @abstractmethod
    async def trade(self):
        """trade"""
