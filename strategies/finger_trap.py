import asyncio

from mql.trader import DealTrader
from mql.symbol import Symbol
from mql.strategy import Strategy, Entry
from mql.constants import TimeFrame, OrderType
from mql.candle import Candle, Candles
from mql.account import Account


class FTCandle(Candle):
    def ema_crossover(self):
        return self.open < self.ema < self.close

    def ema_cross_under(self):
        return self.open > self.ema > self.close


class FingerTrap(Strategy):
    trend_time_frame: TimeFrame = TimeFrame.M30
    entry_time_frame: TimeFrame = TimeFrame.M5
    trend: int = 3
    fast_period: int = 8
    slow_period: int = 34
    Candle = FTCandle

    def __init__(self, *, symbol: Symbol, account: Account):
        self.fast_period = self.fast_period
        self.slow_period = self.slow_period
        self.trend_time_frame = self.trend_time_frame
        self.entry_time_frame = self.entry_time_frame
        self.trend = self.trend
        self.trader = DealTrader(account=account, symbol=symbol)
        self.name = "FingerTrap"
        super().__init__(symbol=symbol)

    @property
    def parameters(self):
        return {
            "name": self.name,
            "symbol": self.symbol.name,
            "fast_period": self.fast_period,
            "slow_period": self.slow_period,
            "trend_time": self.trend_time_frame,
            "entry_time": self.entry_time_frame,
            "trend": self.trend,
        }

    async def check_trend(self):
        fast: Candles
        slow: Candles
        fast, slow = await asyncio.gather(self.get_ema(time_frame=self.trend_time_frame, period=self.fast_period),
                                          self.get_ema(time_frame=self.trend_time_frame, period=self.slow_period))

        fast: list[FTCandle] = [candle for candle in fast[1:self.trend+1]]
        slow: list[FTCandle] = [candle for candle in slow[1:self.trend+1]]

        uptrend = all((s.ema < f.ema < f.close) for f, s in zip(fast, slow))
        if uptrend:
            return Entry(trend='uptrend', time=self.entry_time_frame.time, type=OrderType.BUY)

        downtrend = all((s.ema > f.ema > f.close) for f, s in zip(fast, slow))
        if downtrend:
            return Entry(trend='downtrend', time=self.entry_time_frame.time, type=OrderType.SELL)

        return Entry(current=fast[0].time, time=self.trend_time_frame.time)

    async def confirm_trend(self) -> Entry:
        entry = await self.check_trend()
        if entry.trend == 'notrend':
            if self.current == entry.current:
                return Entry(new=False)
            self.current = entry.current
            return entry

        prices: Candles = await self.get_ema(time_frame=self.entry_time_frame, period=self.fast_period)
        entry_candle: FTCandle = prices[1]

        if self.current == entry_candle.time:
            return Entry(new=False)
        else:
            self.current = entry_candle.time

        if entry.trend == 'uptrend' and entry_candle.ema_crossover():
            return entry

        if entry.trend == 'downtrend' and entry_candle.ema_cross_under():
            return entry

        return Entry(time=self.trend_time_frame.time)

    async def trade(self):
        while True:
            try:
                entry = await self.confirm_trend()
                print(self.symbol, entry.trend, '\n')

                if not entry.new:
                    await asyncio.sleep(0.5)
                    continue

                if not entry.type:
                    await self.sleep(entry.time)
                    continue

                await self.trader.place_trade(order=entry.type, params=self.parameters)
                await self.sleep(entry.time)
            except Exception as err:
                # print(self.symbol, err, "\n")
                await self.sleep(self.entry_time_frame.time)
                continue
