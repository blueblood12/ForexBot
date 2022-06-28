from concurrent.futures import ThreadPoolExecutor
import asyncio
import pprint

import MetaTrader5 as mt5

from account import Account
from symbol import Symbol, Synthetic
from constants import TimeFrame

if not mt5.initialize():
    print("Unable to initialize terminal")
    quit()

account = Account(login=5054652, password="nwa0#anaEze", server="Deriv-Demo", risk=0.03, risk_to_reward=2)

if not account.connected:
    print("Unable to connect")
    quit()


async def main():
    sym = Synthetic(name='Volatility 100 (1s) Index')
    pprint.pprint(sym.dict(), indent=5)
    # await sym.limits(volume=0.03, amount=300, risk_to_reward=2)
    # print(sym.ask, sym.pip)
    # rates = await sym.rates_from_pos(time_frame=TimeFrame.M5, count=50,)
    # pprint.pprint(rates)


asyncio.run(main())
