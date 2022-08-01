from . import Base
from utils.record import save_to_csv


class MqlTradeResult(Base):
    retcode: int
    deal: int
    order: int
    volume: float
    price: str
    bid: float
    ask: float
    comment: str
    request: dict
    request_id: int
    retcode_external: int

    async def record_trade(self, **kwargs):
        try:
            kwargs.update(volume=self.volume, order=self.order, deal=self.deal)
            name = kwargs.pop('name')
            await save_to_csv(name, kwargs)
        except Exception as err:
            print(err)


class MqlTradeCheck(Base):
    retcode: int
    balance: float
    equity: float
    margin: float
    margin_free: float
    margin_level: float
    comment: str
