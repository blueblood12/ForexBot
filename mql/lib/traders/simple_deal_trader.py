# import logging
import datetime

from ... import dict_to_string
from ...result import TradeResult
from ...symbol import Symbol
from ...trader import Trader
from ...core.constants import OrderType


class DealTrader(Trader):

    def __init__(self, *, symbol: type(Symbol), volume=0.01):
        super().__init__(symbol=symbol)
        self.volume = volume
        self.symbol = symbol

    async def create_order(self, order: OrderType, points: float):
        await self.account.refresh()
        amount = self.account.equity * self.account.risk
        sl, tp, volume = await self.symbol.get_sl_tp_volume(amount=amount, risk_to_reward=self.account.risk_to_reward, points=points)
        self.order.volume = volume
        self.order.type = order
        await self.set_order_limits(sl, tp)

    async def set_order_limits(self, sl, tp):
        tick = await self.symbol()
        if self.order.type == OrderType.BUY:
            self.order.sl, self.order.tp = tick.ask - sl, tick.ask + tp
            self.order.price = tick.ask
        else:
            self.order.sl, self.order.tp = tick.bid + sl, tick.bid - tp
            self.order.price = tick.bid

    async def place_trade(self, order: OrderType, points: float, params: dict = None):
        try:
            params = params or {}
            await self.create_order(order=order, points=points)

            check = await self.order.check()
            if check.retcode != 0:
                print(check.comment)
                # logging.warning(f"{check.comment}", extra={"parameters": dict_to_string(params | self.order.dict), "symbol": self.order.symbol})
                return

            result = await self.order.send()
            if result.retcode != 10009:
                print(result.comment)
                # logging.warning(f"{result.comment}", extra={"parameters": dict_to_string(params | self.order.dict), "symbol": self.order.symbol})
                return

            # logging.info(f"{result.comment}", extra={"parameters": dict_to_string(params | self.order.dict), "symbol": self.order.symbol})
            print(result.comment)
            self.order.set_attributes(**result.get_dict(include={'price', 'volume'}))
            result.profit = await self.order.calc_profit()
            TradeResult(parameters=params, request=self.order, result=result, check=check, time=datetime.datetime.utcnow().timestamp())
            return
        except Exception as err:
            print(err)
            # logging.error(err, extra={"parameters": dict_to_string(params | self.order.dict), "symbol": self.order.symbol})
