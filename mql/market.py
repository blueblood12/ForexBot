import asyncio
from abc import ABC

import MetaTrader5 as mt5

from .symbol import Symbol
from .account import Account


class Market(ABC):
    symbols = set()

    def __init__(self, *, account: Account, symbol: type(Symbol), path=""):
        self.account = account
        self.instruments: set[symbol] = set()
        self.symbol = symbol
        self.data = {name: self.symbol(name=name) for name in self.symbols}
        self.connected = False
        self.path = path

    def select_all(self):
        self.instruments = set(self.data.values())

    def select(self, *symbols):
        symbols = set(self.data.values()).intersection(symbols)
        self.instruments.update(symbols)

    async def init(self):
        # init = lambda path: mt5.initialize(path) if self.path else mt5.initialize
        if await asyncio.to_thread(mt5.initialize):
            self.connected = await self.account.account_login()
            if self.connected:
                [await symbol.init() for symbol in self.instruments]
                return self.connected
            return False
        return False

