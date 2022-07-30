import asyncio
import MetaTrader5 as mt5
# import pandas
from pandas import DataFrame
import pandas_ta as ta
from mql.symbol import Symbol
from mql.constants import TimeFrame


async def init():
    mt5.initialize()
    if not mt5.login(login=5050656, password="nwa0#anaEze", server="Deriv-Demo"):
        print("Unable to connect")
        quit('')


async def main():
    await init()
    sym = Symbol(name='EURUSD')
    res = await sym.init()
    rates: DataFrame = await sym.rates_from_pos(time_frame=TimeFrame.M5)
    rates.rename(columns={"tick_volume": "volume"}, inplace=True)
    rates.ta.ad(append=True)
    rates.rename(columns={"AD": "ad"}, inplace=True)
    # print(help(rates.rename))
    print(rates)


asyncio.run(main())
