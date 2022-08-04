from mql.constants import TimeFrame
from mql.symbol import Symbol
from strategies.finger_trap import FingerTrap
from traders.scalp_trader import ScalpTrader


class FingerTrapScalper(FingerTrap):
    trend_time_frame: TimeFrame = TimeFrame.M5
    entry_time_frame: TimeFrame = TimeFrame.M1
    points: float = 30
    expiration: int = 5
    trend = 3
    amount: float = 2
    name = "FingerTrapScalper"

    def __init__(self, *, symbol: Symbol):
        super().__init__(symbol=symbol)
        self.trader = ScalpTrader(symbol=symbol, expiration=self.expiration)

    async def get_support(self):
        self.entry.points = self.points

    def set_params(self, **params):
        self.trader.amount = params.get('amount') or self.amount
        [setattr(self, key, value) for key, value in params.items()]

