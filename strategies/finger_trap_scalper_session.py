import asyncio
from datetime import datetime, timedelta

import pytz

from mql.constants import TimeFrame
from mql.symbol import Symbol
from strategies.finger_trap import FingerTrap
from traders.scalp_trader import ScalpTrader


class FingerTrapSession(FingerTrap):
    trend_time_frame: TimeFrame = TimeFrame.M5
    entry_time_frame: TimeFrame = TimeFrame.M1
    points: float = 30
    expiration: int = 5
    trend = 3
    amount: float = 2
    name = "FingerTrapSession"

    def __init__(self, *, symbol: Symbol):
        super().__init__(symbol=symbol)
        self.trader = ScalpTrader(symbol=symbol, expiration=self.expiration)

    async def get_support(self):
        self.entry.points = self.points

    def set_params(self, **params):
        self.trader.amount = params.get('amount') or self.amount
        [setattr(self, key, value) for key, value in params.items()]

    async def check_time(self):
        now = datetime.now(pytz.timezone("Europe/London"))
        lstart = datetime(year=now.year, month=now.month, day=now.day, hour=8, minute=10, second=0, tzinfo=pytz.timezone("Europe/London"))
        lend = datetime(year=now.year, month=now.month, day=now.day, hour=12, minute=10, second=0, tzinfo=pytz.timezone("Europe/London"))
        nstart = datetime(year=now.year, month=now.month, day=now.day, hour=13, minute=10, second=0, tzinfo=pytz.timezone("Europe/London"))
        nend = datetime(year=now.year, month=now.month, day=now.day, hour=18, minute=10, second=0, tzinfo=pytz.timezone("Europe/London"))
        if lstart < now < lend or nstart < now < nend:
            return True
        if now > nend:
            sl = (lstart + timedelta(hours=24)) - now
        elif now < lstart:
            sl = lstart - now
        else:
            sl = nstart - now
        print(f"sleeping for {sl.seconds}")
        await asyncio.sleep(sl.seconds)
        return False

    async def trade(self):
        while True:
            try:
                if not await self.check_time():
                    continue
                await self.confirm_trend()
                print(self.symbol, self.entry.trend,  '\n')

                if not self.entry.new:
                    await asyncio.sleep(0.5)
                    continue

                if self.entry.type is None:
                    await self.sleep(self.entry.time)
                    continue

                await self.trader.place_trade(order=self.entry.type, points=self.entry.points, params=self.parameters)
                await self.sleep(self.entry.time)
            except Exception as err:
                print(self.symbol, err, "\n")
                await self.sleep(self.trend_time_frame.time)
                continue
