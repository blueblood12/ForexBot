import os
from pathlib import Path
from sys import _getframe
from typing import Iterator, Literal
import json
from functools import cache


class Config:
    login: int
    password: str
    server: str

    def __new__(cls, *args, **kwargs):
        if hasattr(cls, '_instance'):
            return cls._instance
        cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, file: str = ''):
        self.keep_logs = True
        self.record_trades = False
        self.executor: Literal['thread', 'process'] = 'thread'
        self.update_trade_records = self.record_trades and True
        self.filename = "mt5.json"
        self.file = file
        self.load_json()
        self.base: Path = Path.home()
    
    def __setattr__(self, key, value):
        if key == 'base':
            super().__setattr__(key, Path(value))
        super().__setattr__(key, value)

    def find_config(self):
        current_file = __file__
        frame = _getframe()
        while frame.f_code.co_filename == current_file:
            if frame.f_back is None:
                return False
            frame = frame.f_back
        frame_filename = frame.f_code.co_filename
        path = os.path.dirname(os.path.abspath(frame_filename))

        for dirname in self.walk_to_root(path):
            check_path = os.path.join(dirname, self.filename)
            if os.path.isfile(check_path):
                self.file = check_path
                return True
        return False

    def load_json(self):
        res = self.file or self.find_config()
        if not res:
            return
        fh = open(self.file, mode='r')
        data = json.load(fh)
        [setattr(self, key, value) for key, value in data.items()]

    @cache
    def load(self, file: str):
        fh = open(file, mode='r')
        data = json.load(fh)
        [setattr(self, key, value) for key, value in data.items()]

    def set_attributes(self, **kwargs):
        [setattr(self, i, j) for i, j in kwargs.items()]

    @staticmethod
    def walk_to_root(path: str) -> Iterator[str]:

        if not os.path.exists(path):
            raise IOError('Starting path not found')

        if os.path.isfile(path):
            path = os.path.dirname(path)

        last_dir = None
        current_dir = os.path.abspath(path)
        while last_dir != current_dir:
            yield current_dir
            parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
            last_dir, current_dir = current_dir, parent_dir
