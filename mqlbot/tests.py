from concurrent.futures import ThreadPoolExecutor
import asyncio
from pprint import pprint as pp

import MetaTrader5 as mt5

from account import Account
from symbol import Symbol, Synthetic
from constants import TimeFrame as tf

if not mt5.initialize():
    print("Unable to initialize terminal")
    quit()

account = Account(login=5054652, password="nwa0#anaEze", server="Deriv-Demo", risk=0.03, risk_to_reward=2)

if not account.connected:
    print("Unable to connect")
    quit()


async def main():
    sym = Synthetic(name='Volatility 100 (1s) Index')
    df = await sym.rates_from_pos(time_frame=tf.H1)
    ti = df['time']
    pp(list(ti.items()))
    print(1658347200 in (i[1] for i in ti.items()))


asyncio.run(main())
