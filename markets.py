from mql.symbol import Symbol, Synthetic
from mql.market import Market, Account


class Forex(Market):
    symbols = {'AUDCAD', 'AUDJPY' 'AUDNZD', 'AUDUSD', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'CADCHF', 'CADJPY', 'CHFJPY', 'GBPCAD',
               'EURUSD', 'GBPAUD', 'GBPCHF', 'GBPJPY', 'GBPUSD', 'NZDCAD', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY'}

    def __init__(self, *, account: Account):
        super().__init__(account=account, symbol=Symbol)


class Volatility(Market):
    symbols = {'Volatility 10 Index', 'Volatility 25 Index', 'Volatility 50 Index', 'Volatility 75 Index', 'Volatility 100 Index',
               'Volatility 10 (1s) Index', 'Volatility 25 (1s) Index', 'Volatility 50 (1s) Index', 'Volatility 75 (1s) Index',
               'Volatility 100 (1s) Index'}

    def __init__(self, *, account: Account):
        super().__init__(account=account, symbol=Synthetic)
