import asyncio

import MetaTrader5 as mt5
from pandas import DataFrame

from . import Base
from .constants import TimeFrame

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
    selected: bool
    currency_base: str
    currency_profit: str  # quote currency

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"{self.name}"

    def __eq__(self, other: "Symbol"):
        return self.name == other.name

    def __lt__(self, other: "Symbol"):
        return self.name > other.name

    def __hash__(self):
        return hash(self.name)

    async def tick(self):
        tick = await asyncio.to_thread(mt5.symbol_info_tick, self.name)
        self.set_attributes(**tick._asdict())
        return self

    async def select(self):
        state = await asyncio.to_thread(mt5.symbol_select, self.name, True)
        self.visible = self.selected = state

    async def info(self):
        info = await asyncio.to_thread(mt5.symbol_info, self.name)
        if info:
            self.set_attributes(**info._asdict())

    async def init(self):
        await self.select()
        await self.info()

    async def rates_from_pos(self, *, time_frame: TimeFrame, count: int = 500, start_position: int = 0) -> DataFrame:
        rates = await asyncio.to_thread(mt5.copy_rates_from_pos, self.name, time_frame, start_position, count)
        return DataFrame(rates)

    def get_volume(self, amount, points):
        vol = amount / (points * 100000 * self.point)
        return round(max(vol, self.volume_min), 2)

    async def get_limits(self, *, amount: float, risk_to_reward: float, points: float):
        amount = amount if self.currency_profit == "USD" else await self.dollar_to_currency(amount)
        volume = self.get_volume(amount, points)
        point_value = volume * self.point * 100000
        points = (amount / point_value) * self.point
        stop_loss, take_profit = points, points * risk_to_reward
        return stop_loss, take_profit, volume

    async def dollar_to_currency(self, amount: float) -> float:
        if (symbol := f"{self.currency_profit}USD") in dollar_pairs:
            tick = await Symbol.get_tick(symbol)
            return amount / tick.ask
        tick = await Symbol.get_tick(f"USD{self.currency_profit}")
        return amount * tick.ask

    @classmethod
    async def get_tick(cls, name):
        return await asyncio.to_thread(mt5.symbol_info_tick, name)


class Synthetic(Symbol):

    def get_volume(self, amount, points):
        vol = (points * self.point) / amount
        return round(max(vol, self.volume_min), 2)

    async def get_limits(self, *, amount: float, risk_to_reward: float,  points: float):
        volume = self.get_volume(amount, points)
        return amount / volume, (amount / volume) * risk_to_reward, volume
