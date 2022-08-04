import asyncio

import MetaTrader5 as mt5

from mql.account import Account
from mql.trader import DealTrader
from traders.scalp_trader import ScalpTrader
from mql.symbol import Symbol
from mql.orders import Orders
from mql.constants import OrderType


# account = Account(login=160259109, password="TheN@me0fTheW!nd", server="ForexTimeFXTM-Demo01")
account = Account(login=5050656, password="nwa0#anaEze", server="Deriv-Demo")


async def test_scalp_trader():
    sym = Symbol(name="EURUSD")
    await sym.init()
    trader = ScalpTrader(symbol=sym)
    res = await trader.place_trade(order=OrderType.BUY, points=20)
    print(res.dict)


async def init():
    mt5.initialize()
    if not await account.account_login():
        print("Unable to login")
        return


async def test_get_orders():
    await init()
    o = Orders()
    res = await o.get_order(1579701475)
    ress = [res._asdict() for res in res]
    print(ress[0])

asyncio.run(test_get_orders())
