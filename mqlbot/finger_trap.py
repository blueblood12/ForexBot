import asyncio

from mqltrader import MqlTrader
from analyzer import Analyzer, Entry
from constants import TimeFrame, OrderType
from candle import Candle, Candles


class FingerTrap(Analyzer):
    def __init__(self, symbol: str, trader: MqlTrader, periods: tuple[int, int] = (8, 34), trend_time_frame: TimeFrame = TimeFrame.M5,
                 entry_time_frame: TimeFrame = TimeFrame.M2, trend: int = 2):
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
            return Entry(trend='uptrend')

        downtrend = all((s.ema > f.ema > f.mid) for f, s in zip(fast, slow))
        if downtrend:
            return Entry(trend="downtrend")

        return Entry(trend="notrend", current=fast[0].time)

    async def check_entry(self) -> Entry:
        trend = await self.check_trend()

        if trend.trend == 'notrend':
            if self.current == trend.current:
                return Entry(new=False)
            self.current = trend.current
            return Entry(time=self.trend_time_frame.time)

        prices: Candles = await self.get_ema(time_frame=self.entry_time_frame, period=self.fast_period)
        entry_candle = prices[1]

        if self.current == entry_candle.time:
            return Entry(new=False)
        else:
            self.current = entry_candle.time

        if trend == 'uptrend' and entry_candle.ema_crossover():
            return Entry(trend='uptrend', time=self.entry_time_frame.time, type=OrderType.BUY)

        if trend == 'downtrend' and entry_candle.ema_cross_under():
            return Entry(trend='downtrend', time=self.entry_time_frame.time, type=OrderType.SELL)

        return Entry(time=self.entry_time_frame.time)

    async def trade(self):
        while True:
            try:
                entry = await self.check_entry()
                print(self.symbol, entry.trend, '\n')
                if not entry.new:
                    await asyncio.sleep(0.5)
                    continue

                if not entry.type:
                    await self.sleep(entry.time)
                    continue

                await self.trader.place_trade(symbol=self.symbol, order=entry.type)
                await self.sleep(entry.time)
            except Exception as err:
                print(self.symbol, err, "\n")
                await self.sleep(self.entry_time_frame.time)
                continue
