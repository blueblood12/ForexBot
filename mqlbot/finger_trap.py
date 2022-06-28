import asyncio

from mqltrader import MqlTrader
from analyzer import Analyzer, order
from constants import TimeFrame, OrderType
from candle import Candle, Candles


class FingerTrap(Analyzer):
    def __init__(self, symbol: str, trader: MqlTrader, periods: tuple[int, int] = (8, 34), trend_time_frame: TimeFrame = TimeFrame.M3,
                 entry_time_frame: TimeFrame = TimeFrame.M2, trend: int = 5):
        self.fast_period, self.slow_period = periods
        self.trend_time_frame = trend_time_frame
        self.entry_time_frame = entry_time_frame
        self.trend = trend
        super().__init__(symbol=symbol, trader=trader)
        asyncio.run(self.trade())

    async def check_trend(self):
        fast: Candles
        slow: Candles
        fast, slow = await asyncio.gather(self.get_ema(time_frame=self.trend_time_frame, period=self.fast_period),
                                          self.get_ema(time_frame=self.trend_time_frame, period=self.slow_period))

        fast: list[Candle] = [candle for candle in fast[1:self.trend]]
        slow: list[Candle] = [candle for candle in slow[1:self.trend]]

        uptrend = all((s.ema < f.ema < f.mid) for f, s in zip(fast, slow))
        if uptrend:
            return "uptrend"

        downtrend = all((s.ema > f.ema > f.mid) for f, s in zip(fast, slow))
        if downtrend:
            return "downtrend"

        return 'notrend'

    async def check_entry(self) -> order:
        trend = await self.check_trend()
        if trend == 'notrend':
            return order(time=self.trend_time_frame.time)

        prices: Candles = await self.get_ema(time_frame=self.entry_time_frame, period=self.fast_period)
        entry = prices[0]

        if self.current == entry.time:
            return order(new=False)
        else:
            self.current = entry.time

        if trend == 'uptrend' and entry.ema_crossover():
            return order(time=self.entry_time_frame.time, type=OrderType.BUY)

        if trend == 'downtrend' and entry.ema_cross_under():
            return order(time=self.entry_time_frame.time, type=OrderType.SELL)

        return order(time=self.entry_time_frame.time)

    async def trade(self):
        print(self.symbol, '\n\r')
        while True:
            try:
                entry = await self.check_entry()
                if not entry.new:
                    continue
                if not entry.type:
                    await self.sleep(entry.time)
                asyncio.run_coroutine_threadsafe(self.trader.place_trade(symbol=self.symbol, order=entry.type), asyncio.get_event_loop())
                await self.sleep(self.entry_time_frame.time)
            except Exception as err:
                print(self.symbol, err, "\n\r")
                await self.sleep(self.entry_time_frame.time)
                continue
