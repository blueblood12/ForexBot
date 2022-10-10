import asyncio

from .core.meta_trader import MetaTrader
from .core.models import TradePosition
from .core.constants import TradeAction, OrderType
from .order import Order


class Positions:
    def __init__(self, *, symbol: str = "", group: str = "", ticket: int = 0, mt5=MetaTrader()):
        self.mt5 = mt5
        self.symbol = symbol
        self.group = group
        self.ticket = ticket
        self.total_positions = 0
        self.positions: list[TradePosition] = []

    async def positions_total(self):
        self.total_positions = await self.mt5.positions_total()
        return self.total_positions

    async def positions_get(self):
        positions = await self.mt5.positions_get(group=self.group, symbol=self.symbol, ticket=self.ticket)
        self.positions = [TradePosition(**pos._asdict()) for pos in positions]
        return self.positions

    async def close_all(self):
        orders = [Order(mt5=self.mt5, action=TradeAction.DEAL, price=pos.price_current, position=pos.ticket,
                        type=OrderType(pos.type).opposite,
                        **pos.get_dict(include={'symbol', 'volume'})) for pos in (await self.positions_get())]

        results = await asyncio.gather(*[order.send() for order in orders])
        return len([res for res in results if res.retcode == 10009])
