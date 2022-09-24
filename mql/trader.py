from abc import ABC, abstractmethod

from .account import account
from .order import Order
from .result import TradeResult
from .symbol import Symbol


class Trader(ABC):

    def __init__(self, *, symbol: type(Symbol), **kwargs):
        self.account = account
        self.symbol = symbol
        self.order = Order(symbol=symbol.name)

    @abstractmethod
    async def create_order(self, *args, **kwargs):
        """"""""

    @abstractmethod
    async def place_trade(self, *args, **kwargs) -> TradeResult | None:
        """"""