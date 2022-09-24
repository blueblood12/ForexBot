import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Sequence

from mql.strategy import Strategy


class Executor:
    def __init__(self):
        self.workers: list[type(Strategy)] = []

    def add_workers(self, strategies: Sequence[type(Strategy)]):
        self.workers.extend(strategies)

    def add_worker(self, strategy: type(Strategy)):
        self.workers.append(strategy)

    @staticmethod
    def run(strategy: type(Strategy)):
        asyncio.run(strategy.trade())

    def thread_pool_executor(self):
        with ThreadPoolExecutor(max_workers=len(self.workers)) as executor:
            executor.map(self.run, self.workers)

    def process_pool_executor(self, workers=0):
        max_workers = workers or len(self.workers)
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            executor.map(self.run, self.workers)
