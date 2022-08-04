from mql.constants import TimeFrame, OrderType
from mql.symbol import Symbol
from strategies.finger_trap import FingerTrap
from mql.trader import DealTrader
from mql.candle import Candle, Candles


class FTCandles(Candles):
    def get_swing_high(self) -> None | type(Candle):
        count = 0
        for candle in self[1:-1]:
            if self.is_swing_high(candle) and (count := count+1) == 2:
                return candle

    def get_swing_low(self) -> None | type(Candle):
        count = 2
        for candle in self[1:-1]:
            if self.is_swing_low(candle) and (count := count+1) == 2:
                return candle


class FixedVolumeTrader(DealTrader):
    volume: float = 0.02

    async def create_request(self, order: OrderType, points: float):
        points_value = self.symbol.point * 100000 * self.volume
        sl, tp = points*points_value, points*points_value*2
        self.request.volume = self.volume
        self.request.type = order
        await self.set_price_limits(limits=(sl, tp))


class FingerTrapEbere(FingerTrap):
    trend_time_frame: TimeFrame = TimeFrame.M5
    entry_time_frame: TimeFrame = TimeFrame.M1
    points: float = 30
    expiration: int = 5
    trend = 3
    amount: float = 2
    name = "FingerTrapEbere"
    volume = 0.02
    Candles = FTCandles

    def __init__(self, *, symbol: Symbol):
        super().__init__(symbol=symbol)
        self.trader = FixedVolumeTrader(symbol=symbol)

    def set_params(self, **params):
        self.trader.amount = params.get('volume') or self.volume
        [setattr(self, key, value) for key, value in params.items()]
