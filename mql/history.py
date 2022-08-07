import asyncio
from datetime import datetime, timedelta

import MetaTrader5 as mt5

from . import Base
from mql.strategy import Strategy
from utils.record import update_csv, get_orders


class Deal(Base):
    ticket: int
    order: int
    time: int
    time_msc: float
    type: int
    entry: int
    magic: int
    position_id: int
    reason: int
    volume: float
    price: float
    commission: float
    swap: float
    profit: float
    fee: float
    symbol: str
    comment: str


class Order(Base):
    ticket: int
    order: int
    time_setup: int
    time_setup_msc: float
    time_expiration: float
    type: int
    type_time: int
    type_filling: int
    state: int
    magic: int
    volume_current: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    symbol: str


class History:
    def __init__(self, strategy: str):
        self.strategy = strategy
        self.deals: list[Deal] = []
        self.orders: list[Order] = []
        self.update: dict[int | str, dict | list] = {}

    async def get_deals(self, *, start: float | None = None, end: float | None = None):
        now = datetime.utcnow()
        end = datetime.fromtimestamp(end) if end else now + timedelta(hours=24-now.hour, minutes=-now.minute, seconds=59)
        start = datetime.fromtimestamp(start) if start else end - timedelta(hours=end.hour, minutes=end.minute)
        print(end, start)
        res = await asyncio.to_thread(mt5.history_deals_get, start, end)
        self.deals = [Deal(**deal._asdict()) for deal in res]

    async def get_deal(self, ticket):
        res = await asyncio.to_thread(mt5.history_deals_get, ticket=ticket)
        return res

    async def update_record(self):
        start, orders, fieldnames = await get_orders(self.strategy)
        await self.get_deals(start=start)
        print(orders)
        for deal in self.deals:
            if deal.position_id in orders and deal.profit != 0:
                self.update[deal.position_id] = {"Actual Profit": deal.profit, "Win": deal.profit > 0}
        [fieldnames.append(f) for f in ["Actual Profit", "Win"] if f not in fieldnames]
        self.update['fieldnames'] = fieldnames
        # self.update['fieldnames'] = list(set(fieldnames) | {"Actual Profit", "Win"})

        await update_csv(self.strategy, self.update)
