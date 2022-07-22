
# class Order(Base):
#     ticket: int
#     time_setup: int
#     time_setup_msc: int
#     time_expiration: float
#     type: int
#     type_time: float
#     type_filling: int
#     state: int
#     magic: int
#     volume_current: float
#     price_open: float
#     sl: float
#     tp: float


# class Position(Base):
#     ticket: int
#     type: OrderType
#     magic: int
#     identifier: int
#     volume: float
#     price_open: float
#     sl: float
#     tp: float
#     price_current: float
#     swap: float
#     profit: float
#     symbol: str
#     comment: str
#
#
# class HistoryOrders(Base):
#     ticket: int
#     time_setup: datetime
#     time_setup_msc: int
#     time_done: datetime
#     time_done_msc: int
#     type: OrderType
#     type_filling: OrderFilling
#     price_open: float
#     price_current: float
#     volume_initial: float
#     symbol: str
#     comment: str
#     external_id: int
