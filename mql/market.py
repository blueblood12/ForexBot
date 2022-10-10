from abc import ABC

from .core.meta_trader import MetaTrader
from .core.models import BookInfo
from .symbol import Symbol


class Market(ABC):
    symbols = set()
    name: str = ""
    symbol: type(Symbol) = Symbol

    def __init__(self, *, mt5=MetaTrader()):
        self.mt5 = mt5
        self.trading_symbols: set[type(Symbol)] = set()
        self.symbol = self.symbol
        self.name = self.name or self.__class__.__name__

    def select_all(self):
        self.trading_symbols = {self.symbol(name=symbol) for symbol in self.symbols}

    def select(self, *symbols):
        symbols = self.symbols.intersection(symbols)
        symbols = {self.symbol(name=symbol) for symbol in symbols}
        self.trading_symbols.update(symbols)
        return symbols

    async def book_add(self, symbol: str):
        return await self.mt5.market_book_add(symbol) if symbol in self.trading_symbols else False

    async def book_get(self, symbol: str) -> BookInfo | None:
        if symbol not in self.trading_symbols: return None
        info = await self.mt5.market_book_get(symbol)
        return BookInfo(**info._asdict())

    async def book_release(self, symbol: str):
        return await self.mt5.market_book_release(symbol) if symbol in self.trading_symbols else False

    async def init_symbols(self):
        self.trading_symbols = {symbol for symbol in self.trading_symbols if await symbol.init()}
