from abc import ABC, abstractmethod

from .account import Account
from .request import MqlTradeRequest
from .constants import OrderType
from .symbol import Symbol


class MqlTrader(ABC):

    def __init__(self, *, account: Account, symbol: Symbol):
        self.account = account
        self.symbol = symbol
        self.request = MqlTradeRequest(symbol=symbol.name)

    @abstractmethod
    async def create_request(self, *args, **kwargs):
        """"""""

    @abstractmethod
    async def place_trade(self, *args, **kwargs):
        """"""


class DealTrader(MqlTrader):
    async def create_request(self, order: OrderType):
        ramm = await self.account.get_ramm()
        sl, tp, volume = await self.symbol.levels(**ramm.dict)
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

    async def place_trade(self, order: OrderType, params: dict = None):
        try:
            await self.create_request(order=order)

            res = await self.request.check_order()
            if res.retcode != 0:
                print(res.comment, self.symbol, '\n')
                return

            res = await self.request.send_order()
            if res.retcode != 10009:
                print(res.retcode, res.comment, self.symbol, '\n')
                return

            self.request.price = res.price
            profit = await self.request.calc_profit()
            await res.record_trade(action=str(self.request.action), type=str(self.request.type), profit=profit, **params)
            print(self.symbol, res.comment, '\n')
        except Exception as err:
            print(err, self.symbol, '\n')
