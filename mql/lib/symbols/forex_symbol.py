import math

from ...symbol import Symbol


class ForexSymbol(Symbol):

    dollar_pairs = ('AUDUSD', 'EURUSD', 'GBPUSD', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY')

    def get_volume(self, amount, points):
        vol = amount / (points * 100000 * self.point)
        return round(max(vol, self.volume_min), abs(int(math.log10(self.volume_step))))

    async def get_sl_tp_volume(self, *, amount: float, risk_to_reward: float, points: float):
        amount = amount if self.currency_profit == "USD" else await self.dollar_to_currency(amount)
        volume = self.get_volume(amount, points)
        point_value = volume * self.point * 100000
        points = (amount / point_value) * self.point
        stop_loss, take_profit = points, points * risk_to_reward
        return stop_loss, take_profit, volume

    async def dollar_to_currency(self, amount: float) -> float:
        if (symbol := f"{self.currency_profit}USD") in self.dollar_pairs:
            tick = await self.get_tick(symbol)
            return amount / tick.ask
        tick = await self.get_tick(f"USD{self.currency_profit}")
        return amount * tick.ask
