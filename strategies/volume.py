import asyncio

from mql.trader import DealTrader
from mql.symbol import Symbol
from mql.strategy import Strategy, Entry
from mql.constants import TimeFrame, OrderType
from mql.candle import Candle, Candles
from mql.account import Account


class VCandle(Candle):
    ad: float


class Volume(Strategy):
    hourone: TimeFrame
    entry: Entry
    period: int
    Candle = VCandle

    def __init__(self, symbol: Symbol, account: Account):
        self.hourone = TimeFrame.H1
        self.period = 20
        self.name = "VolumeStrategy"
        super().__init__(symbol=symbol)

    async def get_ad(self):
        data = await self.symbol.rates_from_pos(time_frame=self.hourone)
        data.ta.ad(volume="tick_volume", append=True)
        data.ta.ema(close='AD', append=True)
        data.ta.rename(columns={f"EMA_{self.period}": 'ema', "AD": "ad"}, inplace=True)
        return Candles(data=data, candle=self.Candle)

    async def trade(self):
        """"""

