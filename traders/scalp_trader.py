from mql.trader import DealTrader, Symbol, OrderType


class ScalpTrader(DealTrader):

    def __init__(self, *, symbol: Symbol, expiration=5):
        super().__init__(symbol=symbol)
        self.amount = 2
        self.expiration = expiration * 3600

    async def create_request(self, order: OrderType, points: float):
        ramm = await self.account.compute_ramm()
        ramm.amount = self.amount
        sl, tp, volume = await self.symbol.get_limits(amount=ramm.amount, risk_to_reward=ramm.risk_to_reward, points=points)
        self.request.volume = volume
        self.request.type = order
        await self.set_price_limits(limits=(sl, tp))
