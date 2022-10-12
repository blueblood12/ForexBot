# MetaTrader 5 Bots

- Create your own trading bot using the bot builder and prebuilt strategies.
- Trade on multiple instruments, with multiple strategies concurrently using threapool or process poop executors.
- Keep track of the success of your strategies by optionally saving trades and the parameters of your strategies to csv files.
- Easily build your own strategies by subclassing the strategies and trader classes.

```python
import os

from mql.config import Config
from mql.lib.strategies.finger_trap import FingerTrap
from mql.bot_builder import Bot
from mql.lib.markets.forex_market import ForexMarket
from mql.lib.markets.synthetic_market import SyntheticMarket


config = Config(record_trades=True, login=os.eviron['MT5_LOGIN'], password=os.environ['MT5_PASSWORD'], server=os.environ['MT5_SERVER']))

# select the deriv synthetic market and add it to the bot
market = SyntheticMarket()
bot = Bot(market=market)

# use a sample strategy and run it on all symbols in the deriv synthetic market
bot.add_strategy_all(strategy=FingerTrap)

# run the bot using the default threadpool executor
bot.execute()
```
Detailed Documentation comming soon, contributors and sponsors welcomed.
