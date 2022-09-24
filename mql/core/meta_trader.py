from typing import Iterable
from datetime import datetime
import asyncio

from . import Platform
from .models import AccountInfo, TerminalInfo, SymbolInfo, BookInfo, TradeRequest, OrderCheckResult, TradeOrder, OrderSendResult, TradePosition, TradeDeal
from .constants import TimeFrame, CopyTicks, OrderType


class MetaTrader(Platform):

    async def login(self, login: int, password: str, server: str, timeout: int = 60000) -> bool:
        """"""
        res = await asyncio.to_thread(self._login, login, password=password, server=server, timeout=timeout)
        return res

    async def initialize(self, path: str = "", login: int = 0, password: str = "", server: str = "", timeout: int = 60000, portable=False) -> bool:
        """"""
        args = (path,) if path else tuple()
        kwargs = {key: value for key, value in (('login', login), ('password', password), ('server', server), ('timeout', timeout),
                                                ('portable', portable)) if value}
        res = await asyncio.to_thread(self._initialize, *args, **kwargs)
        return res

    async def shutdown(self):
        """"""
        await asyncio.to_thread(self._shutdown)

    async def version(self) -> tuple[int, int, str] | None:
        """"""
        res = await asyncio.to_thread(self._version)
        return res

    async def account_info(self) -> AccountInfo:
        """"""
        res = await asyncio.to_thread(self._account_info)
        res = res._asdict() if res else {}
        return AccountInfo(**res)

    async def terminal_info(self) -> TerminalInfo:
        res = await asyncio.to_thread(self._terminal_info)
        res = res._asdict() if res else {}
        return TerminalInfo(**res)

    async def symbols_total(self) -> int:
        res = await asyncio.to_thread(self._symbols_total)
        return res

    async def symbols_get(self, group: str = "") -> Iterable[SymbolInfo]:
        kwargs = {'group': group} if group else {}
        symbols = await asyncio.to_thread(self._symbols_get, **kwargs)
        return (SymbolInfo(**symbol._asdict()) for symbol in symbols)

    async def symbol_info(self, symbol: str) -> SymbolInfo:
        symbol = await asyncio.to_thread(self._symbol_info, symbol)
        return SymbolInfo(**symbol._asdict())

    async def symbol_info_tick(self, symbol: str):
        return await asyncio.to_thread(self._symbol_info, symbol)

    async def symbol_select(self, symbol: str, enable: bool) -> bool:
        return await asyncio.to_thread(self._symbol_select, symbol, enable)

    async def market_book_add(self, symbol: str):
        return await asyncio.to_thread(self._market_book_add, symbol)

    async def market_book_get(self, symbol: str) -> BookInfo:
        res = await asyncio.to_thread(self._market_book_get, symbol)
        return BookInfo(**res._asdict())

    async def market_book_release(self, symbol: str) -> bool:
        return await asyncio.to_thread(self._market_book_release, symbol)

    async def copy_rates_from(self, symbol: str, timeframe: TimeFrame, date_from: datetime | int, count: int):
        rates = await asyncio.to_thread(self._copy_rates_from, symbol, timeframe, date_from, count)
        return rates

    async def copy_rates_from_pos(self, symbol: str, timeframe: TimeFrame, start_pos: int, count: int):
        rates = await asyncio.to_thread(self._copy_rates_from_pos, symbol, timeframe, start_pos, count)
        return rates

    async def copy_rates_range(self, symbol: str, timeframe: TimeFrame, date_from: datetime | int, date_to: datetime | int):
        rates = await asyncio.to_thread(self._copy_rates_range, symbol, timeframe, date_from, date_to)
        return rates

    async def copy_ticks_from(self, symbol: str, date_from: datetime | int, count: int, flags: CopyTicks):
        ticks = await asyncio.to_thread(self._copy_ticks_from, symbol, date_from, count, flags)
        return ticks

    async def copy_ticks_from_range(self, symbol: str, date_from: datetime | int, date_to: datetime | int, flags: CopyTicks):
        ticks = await asyncio.to_thread(self._copy_ticks_from_range, symbol, date_from, date_to, flags)
        return ticks

    async def orders_total(self) -> int:
        return await asyncio.to_thread(self._orders_total)

    async def orders_get(self, group: str = "", ticket: int = 0, symbol: str = "") -> Iterable[TradeOrder]:
        kwargs = {key: value for key, value in (('group', group), ('ticket', ticket), ('symbol', symbol)) if value}
        orders = await asyncio.to_thread(self._orders_get, **kwargs)
        return (TradeOrder(**order._asdict()) for order in orders)

    async def order_calc_margin(self, action: OrderType, symbol: str, volume: float, price: float) -> float:
        res = await asyncio.to_thread(self._order_calc_margin, action, symbol, volume, price)
        return res

    async def order_calc_profit(self, action: OrderType, symbol: str, volume: float, price_open: float, price_close: float) -> float:
        res = await asyncio.to_thread(self._order_calc_profit, action, symbol, volume, price_open, price_close)
        return res

    async def order_check(self, request: TradeRequest) -> OrderCheckResult:
        res = await asyncio.to_thread(self._order_check, request)
        return OrderCheckResult(**res._asdict())

    async def order_send(self, request: TradeRequest) -> OrderSendResult:
        res = await asyncio.to_thread(self._order_send, request)
        return OrderSendResult(**res._asdict())

    async def positions_total(self) -> int:
        return await asyncio.to_thread(self._positions_total)

    async def positions_get(self, group: str = "", ticket: int = 0, symbol: str = "") -> Iterable[TradePosition]:
        kwargs = {key: value for key, value in (('group', group), ('ticket', ticket), ('symbol', symbol)) if value}
        positions = await asyncio.to_thread(self._positions_get, **kwargs)
        return (TradePosition(**position._asdict()) for position in positions)

    async def history_orders_total(self, date_from: datetime | int, date_to: datetime | int) -> int:
        return await asyncio.to_thread(self._history_orders_total, date_from, date_to)

    async def history_orders_get(self, date_from: datetime | int, date_to: datetime | int, group: str = "", ticket: int = 0, position: int = 0) -> Iterable[TradeOrder]:
        kwargs = {key: value for key, value in (('group', group), ('ticket', ticket), ('position', position)) if value}
        orders = await asyncio.to_thread(self._history_orders_get, date_from, date_to, **kwargs)
        return (TradeOrder(**order._asdict()) for order in orders)

    async def history_deals_total(self, date_from: datetime | int, date_to: datetime | int) -> int:
        return await asyncio.to_thread(self._history_deals_total, date_from, date_to)

    async def history_deals_get(self, date_from: datetime | int, date_to: datetime | int, group: str = "", ticket: int = 0, position: int = 0) -> Iterable[TradeDeal]:
        kwargs = {key: value for key, value in (('group', group), ('ticket', ticket), ('position', position)) if value}
        deals = await asyncio.to_thread(self._history_deals_get, date_from, date_to, **kwargs)
        return (TradeDeal(**deal._asdict()) for deal in deals)
