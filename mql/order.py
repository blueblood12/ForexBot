from .core.meta_trader import MetaTrader
from .core.models import TradeRequest, OrderSendResult, OrderCheckResult
from .core.constants import TradeAction, OrderTime, OrderFilling


class Order(TradeRequest):
    action: TradeAction = TradeAction.DEAL
    type_time: OrderTime = OrderTime.DAY
    type_filling: OrderFilling = OrderFilling.FOK

    def __init__(self, mt5=MetaTrader(), **kwargs):
        self.mt5 = mt5
        super().__init__(**kwargs)

    async def check(self) -> OrderCheckResult:
        return await self.mt5.order_check(self.dict)

    async def send(self) -> OrderSendResult:
        return await self.mt5.order_send(self.dict)

    async def calc_margin(self) -> float | None:
        return await self.mt5.order_calc_margin(self.type, self.symbol, self.volume, self.price)

    async def calc_profit(self) -> float | None:
        return await self.mt5.order_calc_profit(self.type, self.symbol, self.volume, self.price, self.tp)
