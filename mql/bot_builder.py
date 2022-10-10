import asyncio
from typing import Sequence, Type
import logging

from .core.meta_trader import MetaTrader
from .executor import Executor
from .account import account
from .market import Market
from .symbol import Symbol
from .strategy import Strategy
from .config import Config

logger = logging.getLogger()


class Bot:
    def __init__(self, *, market: Market, mt5=MetaTrader()):
        self.config = Config()
        self.account = account
        self.account.set_attributes(login=self.config.login, password=self.config.password, server=self.config.server)
        self.executor = Executor()
        self.market = market
        self.mt5 = mt5

    def add_symbol_from_market(self, symbol: type(Symbol)):
        self.market.select(symbol)

    def add_all_market_symbols(self):
        self.market.select_all()

    def create_records_dir(self):
        self.config.records_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        init = await self.mt5.initialize(login=self.account.login, server=account.server, password=account.password)
        if not init:
            logger.error("Unable to initialize terminal")
            exit(0)
        logger.info("Initialized Terminal")

        connect = await self.account.account_login()
        if not connect:
            logger.error("Unable to login into to account terminal")
            exit(0)
        logger.info("Login Successful")

        await self.market.init_symbols()

    def execute(self):
        asyncio.run(self.initialize())

        if self.config.record_trades:
            self.create_records_dir()

        print("Starting thr Bot")
        self.executor.execute()

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
