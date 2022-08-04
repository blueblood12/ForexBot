import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Sequence

from mql.strategy import Strategy


class Executor:
    def __init__(self):
        self.workers: list[Strategy] = []

    def add_workers(self, strategies: Sequence[Strategy]):
        self.workers.extend(strategies)

    def add_worker(self, strategy: Strategy):
        self.workers.append(strategy)

    @staticmethod
    def run(strategy: Strategy):
        asyncio.run(strategy.trade())

    def execute(self):
        workers = len(self.workers)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            executor.map(self.run, self.workers)
