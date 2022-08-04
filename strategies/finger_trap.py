import asyncio

from mql.trader import DealTrader
from mql.symbol import Symbol
from mql.strategy import Strategy, Entry
from mql.constants import TimeFrame, OrderType
from mql.candle import Candle, Candles


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
    prices: Candles
    entry: Entry
    name = "FingerTrap"

    def __init__(self, *, symbol: Symbol):
        self.trader = DealTrader(symbol=symbol)
        super().__init__(symbol=symbol)

    @property
    def parameters(self):
        return {
            "name": self.name,
            "symbol": self.symbol.name,
            "fast_period": self.fast_period,
            "slow_period": self.slow_period,
            "trend_time": self.trend_time_frame.time,
            "entry_time": self.entry_time_frame.time,
            "trend": self.trend,
        }

    async def get_support(self):
        if self.entry.trend == 'uptrend':
            sup = self.prices.get_swing_low()
            tick = await self.symbol.tick()
            self.entry.points = (tick.ask - sup.low) / self.symbol.point

        else:
            sup = self.prices.get_swing_high()
            tick = await self.symbol.tick()
            self.entry.points = (sup.high - tick.bid) / self.symbol.point

    async def check_trend(self):
        fast: Candles
        slow: Candles
        fast, slow = await asyncio.gather(self.get_ema(time_frame=self.trend_time_frame, period=self.fast_period),
                                          self.get_ema(time_frame=self.trend_time_frame, period=self.slow_period))

        fast: list[FTCandle] = [candle for candle in fast[1:self.trend + 1]]
        slow: list[FTCandle] = [candle for candle in slow[1:self.trend + 1]]

        uptrend = all((s.ema < f.ema < f.close) for f, s in zip(fast, slow))
        if uptrend:
            self.entry = Entry(trend='uptrend', time=self.entry_time_frame.time, type=OrderType.BUY)
            return

        downtrend = all((s.ema > f.ema > f.close) for f, s in zip(fast, slow))
        if downtrend:
            self.entry = Entry(trend='downtrend', time=self.entry_time_frame.time, type=OrderType.SELL)
            return

        self.entry = Entry(current=fast[0].time, time=self.trend_time_frame.time)

    async def confirm_trend(self):
        await self.check_trend()
        if self.entry.trend == 'notrend':
            if self.current == self.entry.current:
                self.entry.new = False
                return
            self.current = self.entry.current
            return

        self.prices: Candles = await self.get_ema(time_frame=self.entry_time_frame, period=self.fast_period)
        entry_candle: FTCandle = self.prices[1]

        if self.current == entry_candle.time:
            self.entry.new = False
            return
        else:
            self.current = entry_candle.time

        if True or self.entry.trend == 'uptrend' and entry_candle.ema_crossover():
            await self.get_support()
            return

        if True or self.entry.trend == 'downtrend' and entry_candle.ema_cross_under():
            await self.get_support()
            return

        self.entry = Entry(time=self.trend_time_frame.time)

    async def trade(self):
        while True:
            try:
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
                await self.sleep(self.entry_time_frame.time)
                continue
