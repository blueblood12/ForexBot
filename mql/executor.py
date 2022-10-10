import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Sequence

from .strategy import Strategy
from .config import Config


class Executor:
    def __init__(self):
        self.config = Config()
        self.executor = ThreadPoolExecutor if self.config.executor == 'thread' else ProcessPoolExecutor
        self.extras: list = []
        self.workers: list[type(Strategy)] = []

    def add_workers(self, strategies: Sequence[type(Strategy)]):
        self.workers.extend(strategies)

    def add_worker(self, strategy: type(Strategy)):
        self.workers.append(strategy)

    def add_extra_functions(self, func, *args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            self.workers.append((asyncio.run, (func(*args, **kwargs),), {}))
            return
        self.workers.append((func, args, kwargs))

    def submit_extra_functions(self, executor):
        for func in self.extras:
            executor.submit(func[0], *func[1], **func[2])

    @staticmethod
    def run(strategy: type(Strategy)):
        asyncio.run(strategy.trade())

    def execute(self, workers=0):
        workers = (len(self.extras) + len(self.workers)) or workers
        with self.executor(max_workers=workers) as executor:
            executor.map(self.run, self.workers)
            self.submit_extra_functions(executor)
