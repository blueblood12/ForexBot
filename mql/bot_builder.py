import asyncio
from typing import Sequence, Type
# import logging

from .core.meta_trader import MetaTrader
from .executor import Executor
from .account import account
from .market import Market
from .symbol import Symbol
from .strategy import Strategy
from .config import Config

config = Config()


class Bot:
    def __init__(self, *, market: Market, mt5=MetaTrader(), ):
        self.account = account
        self.account.set_attributes(login=config.login, password=config.password, server=config.server)
        self.executor = Executor()
        self.market = market
        self.mt5 = mt5

    def add_symbol_from_market(self, symbol: type(Symbol)):
        self.market.select(symbol)

    def add_all_market_symbols(self):
        self.market.select_all()

    @staticmethod
    def create_records_dir():
        path = config.base / 'trade_records'
        path.mkdir(exist_ok=True)

    async def initialize(self) -> bool:
        await self.mt5.initialize(login=config.login, server=config.server, password=config.password)
        connect = await self.account.account_login()
        if not connect:
            # logging.error("Unable to login")
            return False
        await self.market.init_symbols()
        return True

    def execute(self):
        init = asyncio.run(self.initialize())
        if not init:
            print("Unable to start")
            return

        if config.record_trades:
            self.create_records_dir()

        if config.executor == 'process':
            self.executor.process_pool_executor()
            return
        self.executor.thread_pool_executor()

    def add_strategy(self, strategy: type(Strategy)):
        self.executor.add_worker(strategy)

    def add_strategies(self, strategies: list[type(Strategy)]):
        self.executor.add_workers(strategies)

    def select_all(self):
        self.market.select_all()

    def add_strategy_all(self, *, strategy: Type[Strategy], params: dict | None = None):
        """
        Use this to run a strategy on all available instruments in the market using the default parameters
        :param params:
        :param trader:
        :param strategy:
        :return:
        """
        self.add_all_market_symbols()
        [self.add_strategy(strategy(symbol=symbol, params=params)) for symbol in self.market.trading_symbols]

    def add_strategy_many(self, *, strategy: Type[Strategy], symbols: Sequence[str], params: dict | None = None):
        symbols = self.market.select(*symbols)
        [self.add_strategy(strategy(symbol=symbol, params=params)) for symbol in symbols]
