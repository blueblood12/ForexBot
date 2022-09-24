from ...market import Market
from ..symbols.forex_symbol import ForexSymbol


class ForexMarket(Market):
    symbols = {'AUDCAD', 'AUDJPY' 'AUDNZD', 'AUDUSD', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'CADCHF', 'CADJPY', 'CHFJPY', 'GBPCAD',
                'EURUSD', 'GBPAUD', 'GBPCHF', 'GBPJPY', 'GBPUSD', 'NZDCAD', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY'}

    symbol = ForexSymbol
    name = "Forex Market"

