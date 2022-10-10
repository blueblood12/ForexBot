import logging

from mql.config import Config
from mql.lib.strategies.finger_trap import FingerTrap
from mql.bot_builder import Bot
from mql.lib.markets.forex_market import ForexMarket
from mql.lib.markets.synthetic_market import SyntheticMarket

fmt = "%(asctime)s : %(message)s"

logging.basicConfig(filename='example.log', format=fmt, level=logging.DEBUG)

config = Config()
config.record_trades = True
config.set_attributes(login=21332568, password="nwa0#anaEze", server="Deriv-Demo")

market = SyntheticMarket()
bot = Bot(market=market)
bot.add_strategy_all(strategy=FingerTrap)
bot.execute()
