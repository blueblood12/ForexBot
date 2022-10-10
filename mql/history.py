import asyncio
from datetime import datetime
from typing import Iterable

from .config import Config

from .core.meta_trader import MetaTrader
from .core.models import TradeDeal, TradeOrder


class History:
    deals: Iterable[TradeDeal] | None = None
    orders: Iterable[TradeOrder] | None = None
    total_deals: int = 0
    total_orders: int = 0

    def __init__(self, *, mt5=MetaTrader(), date_from: datetime | float = datetime.utcnow(), date_to: datetime | float = datetime.utcnow(),
                 count: int = 500, group: str = "", ticket: int = 0, position: int = 0):

        self.config = Config()
        self.mt5 = mt5
        self.date_from = date_from
        self.date_to = date_to
        self.count = count
        self.update: dict[int | str, dict | list] = {}
        self.group = group
        self.ticket = ticket
        self.position = position
        self.initialized = False

    async def init(self, deals=True, orders=True):
        tasks = []
        tasks.append(self.get_deals()) if deals else ...
        tasks.append(self.get_orders()) if orders else ...
        res = await asyncio.gather(*tasks)
        self.initialized = all(res)
        return self.initialized

    async def get_deals(self) -> Iterable[TradeDeal]:
        deals = await self.mt5.history_deals_get(date_from=self.date_from, date_to=self.date_to, group=self.group, ticket=self.ticket,
                                                 position=self.position)
        self.deals = (TradeDeal(**deal._asdict()) for deal in deals) if deals else deals
        self.total_deals = len(deals)
        return self.deals

    async def deals_total(self) -> int:
        self.total_deals = await self.mt5.history_deals_total(self.date_from, self.date_to)
        return self.total_deals

    async def get_orders(self) -> Iterable[TradeOrder]:
        orders = await self.mt5.history_orders_get(date_from=self.date_from, date_to=self.date_to, group=self.group, ticket=self.ticket,
                                                   position=self.position)
        self.orders = (TradeOrder(**order._asdict()) for order in orders) if orders else orders
        self.total_orders = len(orders)
        return self.orders

    async def orders_total(self) -> int:
        self.total_orders = await self.mt5.history_orders_total(self.date_from, self.date_to)
        return self.total_orders

