import asyncio
from datetime import datetime
from typing import Iterable
from pathlib import Path
import csv

from .history import History
from .config import Config


class Records:

    def __init__(self, records_dir: Path = None):
        self.config = Config()
        self.records_dir = records_dir or self.config.records_dir

    async def get_records(self):
        for file in self.records_dir.iterdir():
            if file.is_file() and file.name.endswith('.csv'):
                yield file

    async def read_record(self, file: Path):
        with open(file, newline='') as fr:
            reader = csv.DictReader(fr)
            rows = (row for row in reader)
            rows = await self.update_record(rows)
            fr.close()
            if not all(rows):
                return
            fw = open(file, newline='', mode='w')
            writer = csv.DictWriter(fw, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
            fw.close()

    async def update_record(self, rows: Iterable):
        rows = sorted((row for row in rows if not bool(row.get('closed'))), key=lambda row: float(row['time']))
        if not rows:
            return [{}]
        start, end = float(rows[0]['time']), datetime.utcnow().timestamp()
        history = History(date_from=start, date_to=end)
        await history.init(orders=False)
        deals = {str(deal.position_id): deal.profit for deal in history.deals}
        for row in rows:
            if row['order'] not in deals:
                continue
            profit = float(row['profit'])
            actual_profit = deals[row['order']]
            win = actual_profit/profit > self.config.win_percentage
            row.update(actual_profit=actual_profit, closed=True, win=win)
        return rows

    async def update_records(self):
        records = [self.read_record(record) async for record in self.get_records()]
        await asyncio.gather(*records)
