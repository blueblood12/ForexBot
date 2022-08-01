import asyncio
from dataclasses import dataclass, asdict

import MetaTrader5 as mt5

from . import Base


@dataclass
class RAMM:
    volume: float
    amount: float
    risk_to_reward: float

    @property
    def dict(self):
        return asdict(self)


class Account(Base):
    login: int
    password: str
    trade_mode: int
    balance: float
    leverage: float
    profit: float
    point: float
    volume: float = 0.1
    equity: float
    margin: float
    risk: float = 0.05
    risk_to_reward: float = 2
    margin_level: float
    margin_free: float
    currency: str = "USD"
    server: str
    fifo_close: bool
    connected: bool
    market: str = 'financial'

    async def refresh_account(self):
        account = await asyncio.to_thread(mt5.account_info)
        self.set_attributes(**account._asdict())

    async def get_ramm(self) -> RAMM:
        await self.refresh_account()
        return RAMM(self.volume, self.equity*self.risk, self.risk_to_reward)

    async def account_login(self):
        self.connected = await asyncio.to_thread(mt5.login, login=self.login, password=self.password, server=self.server)
        if self.connected:
            await self.refresh_account()
        return self.connected
