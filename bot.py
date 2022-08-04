import asyncio
from typing import Sequence, Mapping

from mql.executor import Executor
from mql.account import Account
from strategies.finger_trap import FingerTrap, Strategy
from strategies.finger_trap_scalper import FingerTrapScalper
from strategies.finger_trap_ebere import FingerTrapEbere

from markets import Forex

account = Account(login=5050656, password="nwa0#anaEze", server="Deriv-Demo")
# account = Account(login=5054652, password="nwa0#anaEze", server="Deriv-Demo", market='synthetic')


class Bot:
    def __init__(self, market: Forex):
        self.market = market
        self.executor = Executor()

    def init(self):
        if not asyncio.run(self.market.init()):
            print("Unable to initialize")
            quit()

    def execute(self):
        self.init()
        self.executor.execute()

    def add_strategy(self, strategy: Strategy):
        self.executor.add_worker(strategy)

    def add_strategies(self, strategies: list[Strategy]):
        self.executor.add_workers(strategies)

    def select_instrument(self, name: str):
        if name in self.market.data:
            symbol = self.market.data[name]
            self.market.select(symbol)
            return symbol

    def select_instruments(self, symbols: Sequence[str]):
        [self.select_instrument(name) for name in symbols]

    def select_all(self):
        self.market.select_all()

    def create_strategy(self, strategy: type(Strategy), symbol: str, **kwargs):
        symbol = self.select_instrument(name=symbol)
        if symbol:
            strategy = strategy(symbol=symbol)
            strategy.set_params(**kwargs)
            self.add_strategy(strategy)

    def add_all_default(self, strategy: type(Strategy)):
        """
        Use this to run a strategy on all available instruments in the market using the default parameters
        :param strategy:
        :return:
        """
        self.select_all()
        [self.create_strategy(strategy, symbol) for symbol in self.market.data.keys()]

    def add_many(self, strategy: type(Strategy), symbols: Sequence[str], parameters: Sequence[Mapping]):
        for symbol, params in zip(symbols, parameters):
            self.create_strategy(strategy, symbol, **params)

    @property
    def instruments(self):
        return self.market.instruments


mart = Forex(account=account)
bot = Bot(market=mart)
bot.add_all_default(FingerTrapEbere)
bot.add_all_default(FingerTrap)
scalpers = ["EURUSD", "USDJPY", "GBPUSD", "AUDUSD"]
params = [{} for i in scalpers]
bot.add_many(FingerTrapScalper, scalpers, params)
bot.execute()
