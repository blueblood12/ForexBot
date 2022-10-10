from .core.meta_trader import MetaTrader
from .core.models import TradeRequest, OrderSendResult, OrderCheckResult
from .core.constants import TradeAction, OrderTime, OrderFilling


class Order(TradeRequest):
    action: TradeAction = TradeAction.DEAL
    type_time: OrderTime = OrderTime.SPECIFIED_DAY
    type_filling: OrderFilling = OrderFilling.FOK

    def __init__(self, mt5=MetaTrader(), **kwargs):
        self.mt5 = mt5
        super().__init__(**kwargs)

    async def check(self) -> OrderCheckResult:
        res = await self.mt5.order_check(self.dict)
        return OrderCheckResult(**res._asdict())

    async def send(self) -> OrderSendResult:
        res = await self.mt5.order_send(self.dict)
        return OrderSendResult(**res._asdict())

    async def calc_margin(self) -> float | None:
        return await self.mt5.order_calc_margin(self.type, self.symbol, self.volume, self.price)

    async def calc_profit(self) -> float | None:
        return await self.mt5.order_calc_profit(self.type, self.symbol, self.volume, self.price, self.tp)
