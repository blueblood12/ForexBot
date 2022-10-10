import asyncio
from pprint import pprint
# from concurrent.futures import ThreadPoolExecutor
from mql.history import History
from mql.records import Records
from mql.config import Config
from mql.core.meta_trader import MetaTrader as mt5
from mql.positions import Positions

config = Config()
# config.records_dir.mkdir()
# print(config.base_dir)


async def main():
    s = mt5()
    await s.initialize(login=21332568, password="nwa0#anaEze", server="Deriv-Demo")
    f = await s.login(login=21332568, password="nwa0#anaEze", server="Deriv-Demo")
    p = Positions()
    po = await p.positions_get()
    await p.close_all()



asyncio.run(main())




