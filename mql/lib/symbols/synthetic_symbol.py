import math

from ...symbol import Symbol


class SyntheticSymbol(Symbol):

    def get_volume(self, amount, points):
        vol = (points * self.point) / amount
        return round(max(vol, self.volume_min), abs(int(math.log10(self.volume_step))))

    async def get_sl_tp_volume(self, *, amount: float, risk_to_reward: float, points: float):
        volume = self.get_volume(amount, points)
        return (sl := amount / volume), sl * risk_to_reward, volume
