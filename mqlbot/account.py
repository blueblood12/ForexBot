import asyncio
from collections import namedtuple

import MetaTrader5 as mt5

from mqlbot import Base


order_details = namedtuple('Details', ['volume', 'amount', 'risk_to_reward'])


class Account(Base):
    login: int
    password: str
    trade_mode: int
    balance: float
    leverage: float
    profit: float
    point: float
    volume: float = 0.03   # 3 micro lots
    equity: float
    margin: float
    risk: float = 0.03    # 3 percent
    risk_to_reward: float = 2
    margin_level: float
    margin_free: float
    currency: str = "USD"
    server: str
    fifo_close: bool
    connected: bool
    market: str = 'financial'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connected = mt5.login(login=self.login, password=self.password, server=self.server)
        if self.connected:
            self.refresh_account()

    def refresh_account(self):
        account = mt5.account_info()._asdict()
        self.set_attributes(**account)

    async def get_details(self):
        await asyncio.to_thread(self.refresh_account)
        return order_details(self.volume, self.equity*self.risk, self.risk_to_reward)
