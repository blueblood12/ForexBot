import asyncio
from collections import namedtuple

import MetaTrader5 as mt5
from pandas import DataFrame

from mqlbot import Base
from constants import TimeFrame

tick = namedtuple('SymbolTick', ['time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real'])

dollar_pairs = ['AUDUSD', 'EURUSD', 'GBPUSD', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY']


class Symbol(Base):
    name: str
    time: int
    bid: float
    ask: float
    bidhigh: float
    bidlow: float
    askhigh: float
    asklow: float
    point: float
    pip: float
    last = 0.0
    volume = 0
    volume_real: float
    volumehigh: float
    volumelow: float
    volume_min: float
    volume_max: float
    volume_step: float
    volume_limit: float
    time_msc: int
    flags: int
    digits: int
    spread: float
    visible: bool
    select: bool
    currency_base: str
    currency_profit: str  # quote currency

    def __init__(self, **kw):
        super().__init__(**kw)
        self.symbol_select()
        self.symbol_info()

    def __repr__(self):
        return f"{self.name}"

    @property
    async def tick(self) -> tick:
        tick_ = await Symbol.get_tick(self.name)
        return tick(**tick_._asdict())

    def symbol_select(self):
        self.visible = self.select = mt5.symbol_select(self.name, True)

    def symbol_info(self):
        info = mt5.symbol_info(self.name)._asdict()
        # info['pip'] = info['point'] * 10
        self.update_attributes(**info)

    async def rates_from_pos(self, *, time_frame: TimeFrame, count: int = 500, start_position: int = 0) -> DataFrame:
        rates = await asyncio.to_thread(mt5.copy_rates_from_pos, self.name, time_frame, start_position, count)
        return DataFrame(rates[::-1])

    async def levels(self, *, volume: float, amount: float, risk_to_reward: float):
        volume = volume if volume >= self.volume_min else self.volume_min
        point_value = volume * self.point * 100000
        amount = amount if self.currency_profit == "USD" else await self.dollar_to_currency(amount)
        points = (amount / point_value) * self.point
        stop_loss, take_profit = points, points * risk_to_reward
        return stop_loss, take_profit, volume

    async def dollar_to_currency(self, amount: float) -> float:
        if (symbol := f"{self.currency_profit}USD") in dollar_pairs:
            tick_ = await Symbol.get_tick(symbol)
            return amount / tick_.ask
        tick_ = await Symbol.get_tick(f"USD{self.currency_profit}")
        return amount * tick_.ask

    @classmethod
    async def get_tick(cls, name):
        tick_ = await asyncio.to_thread(mt5.symbol_info_tick, name)
        return tick(**tick_._asdict())


class Synthetic(Symbol):

    async def levels(self, *, volume: float, amount: float, risk_to_reward: float):
        volume = volume if volume >= self.volume_min else self.volume_min
        return amount/volume, (amount/volume) * risk_to_reward, volume

# async def limits(self, *, volume: float, amount: float, risk_to_reward: float):
#     volume = volume if volume >= self.volume_min else self.volume_min
#     pip_value = volume * self.pip * 100000
#     amount = amount if self.currency_profit == "USD" else await self.dollar_to_currency(amount)
#     pips = (amount / pip_value) * self.pip
#     stop_loss, take_profit = pips, pips * risk_to_reward
#     return stop_loss, take_profit, volume