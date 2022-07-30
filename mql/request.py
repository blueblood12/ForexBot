import asyncio
from datetime import datetime

import MetaTrader5 as mt5

from . import Base
from .constants import TradeAction, OrderType, OrderTime, OrderFilling
from .result import MqlTradeResult, MqlTradeCheck


class MqlTradeRequest(Base):
    action: TradeAction = TradeAction.DEAL
    type: OrderType
    order: int
    symbol: str
    volume: float
    sl: float
    tp: float
    price: float
    deviation: float
    stop_limit: float
    type_time: OrderTime = OrderTime.DAY
    type_filling: OrderFilling = OrderFilling.FOK
    expiration: datetime
    position: int
    position_by: int
    comment: str
    magic: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_attributes(action=self.action, type_time=self.type_time, type_filling=self.type_filling)

    async def check_order(self) -> MqlTradeCheck:
        result = await asyncio.to_thread(mt5.order_check, self.dict)
        return MqlTradeCheck(**result._asdict())

    async def send_order(self) -> MqlTradeResult:
        result = await asyncio.to_thread(mt5.order_send, self.dict)
        return MqlTradeResult(**result._asdict())

    async def calc_margin(self) -> float | None:
        return await asyncio.to_thread(mt5.order_calc_margin, self.type, self.symbol, self.volume, self.price)

    async def calc_profit(self) -> float | None:
        return await asyncio.to_thread(mt5.order_calc_profit, self.type, self.symbol, self.volume, self.price, self.tp)
