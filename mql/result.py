import datetime
from functools import cache
import csv
import asyncio

from .core.models import OrderSendResult, OrderCheckResult
from .order import Order
from .config import Config

config = Config()


class TradeResult:

    def __init__(self, result: OrderSendResult, check: OrderCheckResult, request: Order, parameters: dict, time: float):
        self.result = result
        self.check = check
        self.request = request
        self.parameters = parameters
        self.time = time
        self.name = self.parameters.get('name') or datetime.datetime.today().strftime('%d/%m/%Y')
        self.filepath = config.base / 'trade_records'
        if config.record_trades:
            loop = asyncio.get_running_loop()
            asyncio.run_coroutine_threadsafe(self.to_csv(), loop)

    @property
    @cache
    def data(self) -> dict:
        data = self.parameters | self.result.dict |\
               {'actual_profit': 0, 'time': self.time} | self.request.get_dict(include={'action', 'symbol', 'sl', 'tp', 'type'})
        return data

    async def to_csv(self):
        try:
            file = self.filepath / f"{self.name}.csv"
            exists = file.exists()
            self.data.pop('name')
            self.data['date'] = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M")
            with open(file, 'a', newline='') as fh:
                writer = csv.DictWriter(fh, fieldnames=sorted(list(self.data.keys())), extrasaction='ignore', restval=None)
                if not exists:
                    writer.writeheader()
                writer.writerow(self.data)
        except Exception as err:
            print(err)
