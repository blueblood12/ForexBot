from abc import ABC, abstractmethod

from .account import Account
from .request import MqlTradeRequest
from .constants import OrderType
from .symbol import Symbol


class MqlTrader(ABC):

    def __init__(self, *, symbol: Symbol):
        self.account = Account()
        self.symbol = symbol
        self.request = MqlTradeRequest(symbol=symbol.name)

    @abstractmethod
    async def create_request(self, *args, **kwargs):
        """"""""

    @abstractmethod
    async def place_trade(self, *args, **kwargs):
        """"""


class DealTrader(MqlTrader):
    async def create_request(self, order: OrderType, points: float):
        ramm = await self.account.compute_ramm()
        sl, tp, volume = await self.symbol.get_limits(amount=ramm.amount, risk_to_reward=ramm.risk_to_reward, points=points)
        self.request.volume = volume
        self.request.type = order
        await self.set_price_limits(limits=(sl, tp))

    async def set_price_limits(self, limits: tuple[float, float]):
        await self.symbol.tick()
        sl, tp = limits
        if self.request.type == OrderType.BUY:
            self.request.sl, self.request.tp = self.symbol.ask - sl, self.symbol.ask + tp
            self.request.price = self.symbol.ask
        else:
            self.request.sl, self.request.tp = self.symbol.bid + sl, self.symbol.bid - tp
            self.request.price = self.symbol.bid

    async def place_trade(self, order: OrderType, points: float, params: dict = None):
        try:
            params = {} if params is None else params
            await self.create_request(order=order, points=points)

            res = await self.request.check_order()
            if res.retcode != 0:
                print(res.comment, self.symbol, '\n')
                return

            res = await self.request.send_order()
            if res.retcode != 10009:
                print(res.retcode, res.comment, self.symbol, '\n')
                return

            profit = await self.request.calc_profit()

            await res.record_trade(action=str(self.request.action), type=str(self.request.type), expected_profit=profit, **params)
            print(self.symbol, res.comment, '\n')
            return res
        except Exception as err:
            print(err, self.symbol, '\n')
