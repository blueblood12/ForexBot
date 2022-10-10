from datetime import datetime
import asyncio

from . import Platform
from .constants import TimeFrame, CopyTicks, OrderType


class MetaTrader(Platform):

    async def login(self, login: int, password: str, server: str, timeout: int = 60000) -> bool:
        """"""
        return await asyncio.to_thread(self._login, login, password=password, server=server, timeout=timeout)

    async def initialize(self, path: str = "", login: int = 0, password: str = "", server: str = "", timeout: int = 60000, portable=False) -> bool:
        """"""
        args = (path,) if path else tuple()
        kwargs = {key: value for key, value in (('login', login), ('password', password), ('server', server), ('timeout', timeout),
                                                ('portable', portable)) if value}
        return await asyncio.to_thread(self._initialize, *args, **kwargs)

    async def shutdown(self):
        """"""
        return await asyncio.to_thread(self._shutdown)

    async def last_error(self) -> tuple[int, str]:
        return await asyncio.to_thread(self._last_error)

    async def version(self) -> tuple[int, int, str] | None:
        """"""
        return await asyncio.to_thread(self._version)

    async def account_info(self) -> Platform.platform.AccountInfo:
        """"""
        return await asyncio.to_thread(self._account_info)

    async def terminal_info(self) -> Platform.platform.TerminalInfo:
        return await asyncio.to_thread(self._terminal_info)

    async def symbols_total(self) -> int:
        return await asyncio.to_thread(self._symbols_total)

    async def symbols_get(self, group: str = "") -> tuple[Platform.platform.SymbolInfo]:
        kwargs = {'group': group} if group else {}
        return await asyncio.to_thread(self._symbols_get, **kwargs)

    async def symbol_info(self, symbol: str) -> Platform.platform.SymbolInfo:
        return await asyncio.to_thread(self._symbol_info, symbol)

    async def symbol_info_tick(self, symbol: str) -> Platform.platform.Tick:
        return await asyncio.to_thread(self._symbol_info, symbol)

    async def symbol_select(self, symbol: str, enable: bool) -> bool:
        return await asyncio.to_thread(self._symbol_select, symbol, enable)

    async def market_book_add(self, symbol: str) -> bool:
        return await asyncio.to_thread(self._market_book_add, symbol)

    async def market_book_get(self, symbol: str) -> Platform.platform.BookInfo:
        return await asyncio.to_thread(self._market_book_get, symbol)

    async def market_book_release(self, symbol: str) -> bool:
        return await asyncio.to_thread(self._market_book_release, symbol)

    async def copy_rates_from(self, symbol: str, timeframe: TimeFrame, date_from: datetime | int, count: int):
        return await asyncio.to_thread(self._copy_rates_from, symbol, timeframe, date_from, count)

    async def copy_rates_from_pos(self, symbol: str, timeframe: TimeFrame, start_pos: int, count: int):
        return await asyncio.to_thread(self._copy_rates_from_pos, symbol, timeframe, start_pos, count)

    async def copy_rates_range(self, symbol: str, timeframe: TimeFrame, date_from: datetime | int, date_to: datetime | int):
        return await asyncio.to_thread(self._copy_rates_range, symbol, timeframe, date_from, date_to)

    async def copy_ticks_from(self, symbol: str, date_from: datetime | int, count: int, flags: CopyTicks):
        return await asyncio.to_thread(self._copy_ticks_from, symbol, date_from, count, flags)

    async def copy_ticks_from_range(self, symbol: str, date_from: datetime | int, date_to: datetime | int, flags: CopyTicks):
        return await asyncio.to_thread(self._copy_ticks_from_range, symbol, date_from, date_to, flags)

    async def orders_total(self) -> int:
        return await asyncio.to_thread(self._orders_total)

    async def orders_get(self, group: str = "", ticket: int = 0, symbol: str = "") -> tuple[Platform.platform.TradeOrder]:
        kwargs = {key: value for key, value in (('group', group), ('ticket', ticket), ('symbol', symbol)) if value}
        return await asyncio.to_thread(self._orders_get, **kwargs)

    async def order_calc_margin(self, action: OrderType, symbol: str, volume: float, price: float) -> float:
        return await asyncio.to_thread(self._order_calc_margin, action, symbol, volume, price)

    async def order_calc_profit(self, action: OrderType, symbol: str, volume: float, price_open: float, price_close: float) -> float:
        return await asyncio.to_thread(self._order_calc_profit, action, symbol, volume, price_open, price_close)

    async def order_check(self, request: Platform.platform.TradeRequest) -> Platform.platform.OrderCheckResult:
        return await asyncio.to_thread(self._order_check, request)

    async def order_send(self, request: Platform.platform.TradeRequest) -> Platform.platform.OrderSendResult:
        return await asyncio.to_thread(self._order_send, request)

    async def positions_total(self) -> int:
        return await asyncio.to_thread(self._positions_total)

    async def positions_get(self, group: str = "", ticket: int = 0, symbol: str = "") -> tuple[Platform.platform.TradePosition]:
        kwargs = {key: value for key, value in (('group', group), ('ticket', ticket), ('symbol', symbol)) if value}
        return await asyncio.to_thread(self._positions_get, **kwargs)

    async def history_orders_total(self, date_from: datetime | int, date_to: datetime | int) -> int:
        return await asyncio.to_thread(self._history_orders_total, date_from, date_to)

    async def history_orders_get(self, date_from: datetime | int, date_to: datetime | int, group: str = "", ticket: int = 0, position: int = 0) -> \
            tuple[Platform.platform.TradeOrder]:
        kwargs = {key: value for key, value in (('group', group), ('ticket', ticket), ('position', position)) if value}
        return await asyncio.to_thread(self._history_orders_get, date_from, date_to, **kwargs)

    async def history_deals_total(self, date_from: datetime | int, date_to: datetime | int) -> int:
        return await asyncio.to_thread(self._history_deals_total, date_from, date_to)

    async def history_deals_get(self, date_from: datetime | int, date_to: datetime | int, group: str = "", ticket: int = 0, position: int = 0) -> \
            tuple[Platform.platform.TradeDeal]:
        kwargs = {key: value for key, value in (('group', group), ('ticket', ticket), ('position', position)) if value}
        return await asyncio.to_thread(self._history_deals_get, date_from, date_to, **kwargs)
