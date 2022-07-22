from main import Base


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


class MqlTradeCheck(Base):
    retcode: int
    balance: float
    equity: float
    margin: float
    margin_free: float
    margin_level: float
    comment: str
