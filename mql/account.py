from .core.meta_trader import MetaTrader, AccountInfo


class Account(AccountInfo):
    risk: float = 0.05
    risk_to_reward: float = 2
    connected: bool

    def __init__(self, mt5: MetaTrader = MetaTrader(), **kwargs):
        self.mt5 = mt5
        super().__init__(**kwargs)

    async def refresh(self):
        account_info = await self.mt5.account_info()
        self.set_attributes(**account_info.dict)

    async def account_login(self):
        self.connected = await self.mt5.login(login=self.login, password=self.password, server=self.server)
        if self.connected:
            await self.refresh()
        return self.connected


account = Account()
