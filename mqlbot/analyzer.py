import asyncio
import time
from collections import namedtuple

import pandas_ta as ta

from mqltrader import MqlTrader
from constants import TimeFrame, OrderType
from candle import Candle, Candles
from symbol import Symbol, Synthetic

Entry = namedtuple('Entry', ['trend', 'current', 'type', 'time', 'new'], defaults=('notrend', 0, None, 0, True))


class Analyzer:
    count: int

    def __init__(self, symbol: str, trader: MqlTrader):
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
    async def sleep(secs: int):
        await asyncio.sleep(secs - (time.time() % secs) + 1)
