from datetime import datetime, timedelta
from typing import Iterable

from .core import Base
from .core.meta_trader import MetaTrader
from .core.models import TradeDeal, TradeOrder
from mql.strategy import Strategy
from utils.record import update_csv, get_orders


class History:
    deals: Iterable[TradeDeal]
    orders: Iterable[TradeOrder]
    total_deals: float = 0
    total_orders: float = 0

    def __init__(self, mt5=MetaTrader(), date_from: datetime | int = datetime.utcnow(), date_to: datetime | int = datetime.utcnow(), count: int = 500):
        self.mt5 = mt5
        self.date_from = date_from
        self.date_to = date_to
        self.count = count
        self.update: dict[int | str, dict | list] = {}

    async def get_deals(self, group: str = '', ticket: int = 0, position: int = 0):
        self.deals = await self.mt5.history_deals_get(date_from=self.date_from, date_to=self.date_to, group=group, ticket=ticket, position=position)

    async def deals_total(self):
        self.total_deals = await self.mt5.history_deals_total(self.date_from, self.date_to)

    async def get_orders(self, group: str = '', ticket: int = 0, position: int = 0):
        self.orders = await self.mt5.history_orders_get(date_from=self.date_from, date_to=self.date_to, group=group, ticket=ticket, position=position)

    async def orders_total(self):
        self.total_orders = await self.mt5.history_orders_total(self.date_from, self.date_to)

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
