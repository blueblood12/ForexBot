import asyncio
from datetime import datetime, timedelta

import MetaTrader5 as mt5


class Orders:

    async def get_order(self, ticket, start: datetime | None = None, end: datetime | None = None):
        end = end or datetime.now()
        start = start or end - timedelta(hours=end.hour, minutes=end.minute)
        res = await asyncio.to_thread(mt5.history_deals_get, ticket=ticket)
        print(res)
        return res
