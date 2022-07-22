from account import Account
from request import MqlTradeRequest
from constants import OrderType
from symbol import Symbol


class MqlTrader:

    def __init__(self, account: Account):
        self.account = account

    async def create_request(self, symbol: Symbol, order: OrderType) -> MqlTradeRequest:
        order_details = await self.account.get_details()
        sl, tp, volume = await symbol.levels(**order_details._asdict())
        request = MqlTradeRequest(
            symbol=symbol.name,
            type=order,
            volume=volume
        )
        await request.get_price_limits(limits=(sl, tp))
        return request

    async def place_trade(self, symbol: Symbol, order: OrderType):
        try:
            request = await self.create_request(symbol=symbol, order=order)
            res = await request.check_order()
            if res.retcode != 0:
                print(res.comment, symbol, '\n')
                return res
            res = await request.send_order()
            if res.retcode != 10009:
                print(res.retcode, res.comment, symbol, '\n')
            print(symbol, res.comment, '\n')
            return res
        except Exception as err:
            print(err, symbol, '\n')
