import asyncio
from datetime import datetime

import MetaTrader5 as mt5

from mql.account import Account
from mql.trader import DealTrader
from traders.scalp_trader import ScalpTrader
from mql.symbol import Symbol, Synthetic
from mql.history import History
from mql.constants import OrderType
from utils.record import get_orders
from strategies.finger_trap_scalper import FingerTrapScalper

# account = Account(login=160259109, password="TheN@me0fTheW!nd", server="ForexTimeFXTM-Demo01")
# account = Account(login=5050656, password="nwa0#anaEze", server="Deriv-Demo")
account = Account(login=5054652, password="nwa0#anaEze", server="Deriv-Demo", market='synthetic')


async def test_scalp_trader():
    await init()
    sym = Synthetic(name="Volatility 25 Index")
    await sym.init()
    trader = ScalpTrader(symbol=sym)
    res = await trader.place_trade(order=OrderType.BUY, points=30)
    print(datetime.now())
    print(res.dict)


async def init():
    mt5.initialize()
    if not await account.account_login():
        print("Unable to login")
        return


async def test_history():
    await init()
    h = History("FingerTrapScalper")
    await h.update_record()


# async def test_get_deals():
#     await init()
#     start, orders = await get_orders("FingerTrapScalper")
#     o = Orders()
#     res = await o.get_deals(start=start)
#     orders = [int(o) for o in orders]
#     print(orders)
#     # p = [o['position_id'] for o in res]
#     # print(p)
#     e = []
#     for o in res:
#         if o['position_id'] in orders and o['profit'] != 0.0:
#             e.append(o)
#     # print(len(e), len(orders), len(res))
#     print(e[0], len(e))

asyncio.run(test_history())
