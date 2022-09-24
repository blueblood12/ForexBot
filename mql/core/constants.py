from enum import IntEnum

import MetaTrader5 as mt5


class Repr:
    def __str__(self):
        return self.__dict__['_name_']


class TradeAction(Repr, IntEnum):
    DEAL = mt5.TRADE_ACTION_DEAL
    PENDING = mt5.TRADE_ACTION_PENDING
    SLTP = mt5.TRADE_ACTION_SLTP
    MODIFY = mt5.TRADE_ACTION_MODIFY
    REMOVE = mt5.TRADE_ACTION_MODIFY
    CLOSE = mt5.TRADE_ACTION_CLOSE_BY


class OrderFilling(Repr, IntEnum):
    FOK = mt5.ORDER_FILLING_FOK
    IOC = mt5.ORDER_FILLING_IOC
    RETURN = mt5.ORDER_FILLING_RETURN


class OrderTime(Repr, IntEnum):
    GTC = mt5.ORDER_TIME_GTC
    DAY = mt5.ORDER_TIME_DAY
    SPECIFIED = mt5.ORDER_TIME_SPECIFIED
    SPECIFIED_DAY = mt5.ORDER_TIME_SPECIFIED_DAY


class OrderType(Repr, IntEnum):
    BUY = mt5.ORDER_TYPE_BUY
    SELL = mt5.ORDER_TYPE_SELL
    BUY_LIMIT = mt5.ORDER_TYPE_BUY_LIMIT
    SELL_LIMIT = mt5.ORDER_TYPE_SELL_LIMIT
    BUY_STOP = mt5.ORDER_TYPE_BUY_STOP
    SELL_STOP = mt5.ORDER_TYPE_SELL_STOP
    BUY_STOP_LIMIT = mt5.ORDER_TYPE_BUY_STOP_LIMIT
    SELL_STOP_LIMIT = mt5.ORDER_TYPE_SELL_STOP_LIMIT
    CLOSE_BUY = mt5.ORDER_TYPE_CLOSE_BY


class BookType(Repr, IntEnum):
    BOOK_TYPE_SELL = mt5.BOOK_TYPE_SELL
    BOOK_TYPE_BUY = mt5.BOOK_TYPE_BUY
    BOOK_TYPE_SELL_MARKET = mt5.BOOK_TYPE_SELL_MARKET
    BOOK_TYPE_BUY_MARKET = mt5.BOOK_TYPE_BUY_MARKET


class TimeFrame(Repr, IntEnum):
    M1 = mt5.TIMEFRAME_M1
    M2 = mt5.TIMEFRAME_M2
    M3 = mt5.TIMEFRAME_M3
    M4 = mt5.TIMEFRAME_M4
    M5 = mt5.TIMEFRAME_M5
    M6 = mt5.TIMEFRAME_M6
    M10 = mt5.TIMEFRAME_M10
    M15 = mt5.TIMEFRAME_M15
    M20 = mt5.TIMEFRAME_M20
    M30 = mt5.TIMEFRAME_M30
    H1 = mt5.TIMEFRAME_H1
    H2 = mt5.TIMEFRAME_H2
    H3 = mt5.TIMEFRAME_H3
    H4 = mt5.TIMEFRAME_H4
    H6 = mt5.TIMEFRAME_H6
    H8 = mt5.TIMEFRAME_H1
    D1 = mt5.TIMEFRAME_D1
    W1 = mt5.TIMEFRAME_W1
    MN1 = mt5.TIMEFRAME_MN1

    @property
    def time(self):
        times = {1: 60, 2: 120, 3: 180, 4: 240, 5: 300, 6: 360, 10: 600, 15: 900, 20: 1200, 30: 1800, 16385: 3600, 16386: 7200,
                 16387: 10800, 16388: 14400, 16390: 21600, 16392: 21800, 16408: 86400, 32769: 604800, 49153: 2592000}
        return times[self]


class CopyTicks(Repr, IntEnum):
    COPY_TICKS = mt5.COPY_TICKS_ALL
    COPY_TICKS_INFO = mt5.COPY_TICKS_INFO
    COPY_TICKS_TRADE = mt5.COPY_TICKS_TRADE


class PositionType(Repr, IntEnum):
    POSITION_TYPE_BUY = mt5.POSITION_TYPE_BUY
    POSITION_TYPE_SELL = mt5.POSITION_TYPE_SELL


class PositionReason(Repr, IntEnum):
    POSITION_REASON_CLIENT = mt5.POSITION_REASON_CLIENT
    POSITION_REASON_MOBILE = mt5.POSITION_REASON_MOBILE
    POSITION_REASON_WEB = mt5.POSITION_REASON_WEB
    POSITION_REASON_EXPERT = mt5.POSITION_REASON_EXPERT


class DealType(Repr, IntEnum):
    DEAL_TYPE_BUY = mt5.DEAL_TYPE_BUY
    DEAL_TYPE_SELL = mt5.DEAL_TYPE_SELL
    DEAL_TYPE_BALANCE = mt5.DEAL_TYPE_BALANCE
    DEAL_TYPE_CREDIT = mt5.DEAL_TYPE_CREDIT
    DEAL_TYPE_CHARGE = mt5.DEAL_TYPE_CHARGE
    DEAL_TYPE_CORRECTION = mt5.DEAL_TYPE_CORRECTION
    DEAL_TYPE_BONUS = mt5.DEAL_TYPE_BONUS
    DEAL_TYPE_COMMISSION = mt5.DEAL_TYPE_COMMISSION
    DEAL_TYPE_COMMISSION_DAILY = mt5.DEAL_TYPE_COMMISSION_DAILY
    DEAL_TYPE_COMMISSION_MONTHLY = mt5.DEAL_TYPE_COMMISSION_MONTHLY
    DEAL_TYPE_COMMISSION_AGENT_DAILY = mt5.DEAL_TYPE_COMMISSION_AGENT_DAILY
    DEAL_TYPE_COMMISSION_AGENT_MONTHLY = mt5.DEAL_TYPE_COMMISSION_AGENT_MONTHLY
    DEAL_TYPE_INTEREST = mt5.DEAL_TYPE_INTEREST
    DEAL_TYPE_BUY_CANCELED = mt5.DEAL_TYPE_BUY_CANCELED
    DEAL_TYPE_SELL_CANCELED = mt5.DEAL_TYPE_SELL_CANCELED
    DEAL_DIVIDEND = mt5.DEAL_DIVIDEND
    DEAL_DIVIDEND_FRANKED = mt5.DEAL_DIVIDEND_FRANKED
    DEAL_TAX = mt5.DEAL_TAX


class DealEntry(Repr, IntEnum):
    DEAL_ENTRY_IN = mt5.DEAL_ENTRY_IN
    DEAL_ENTRY_OUT = mt5.DEAL_ENTRY_OUT
    DEAL_ENTRY_INOUT = mt5.DEAL_ENTRY_INOUT
    DEAL_ENTRY_OUT_BY = mt5.DEAL_ENTRY_OUT_BY


class DealReason(Repr, IntEnum):
    DEAL_REASON_CLIENT = mt5.DEAL_REASON_CLIENT
    DEAL_REASON_MOBILE = mt5.DEAL_REASON_MOBILE
    DEAL_REASON_WEB = mt5.DEAL_REASON_WEB
    DEAL_REASON_EXPERT = mt5.DEAL_REASON_EXPERT
    DEAL_REASON_SL = mt5.DEAL_REASON_SL
    DEAL_REASON_TP = mt5.DEAL_REASON_TP
    DEAL_REASON_SO = mt5.DEAL_REASON_SO
    DEAL_REASON_ROLLOVER = mt5.DEAL_REASON_ROLLOVER
    DEAL_REASON_VMARGIN = mt5.DEAL_REASON_VMARGIN
    DEAL_REASON_SPLIT = mt5.DEAL_REASON_SPLIT
