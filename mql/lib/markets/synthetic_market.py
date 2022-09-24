from ...market import Market
from ..symbols.synthetic_symbol import SyntheticSymbol


class SyntheticMarket(Market):
    symbols = {'Volatility 10 Index', 'Volatility 25 Index', 'Volatility 50 Index', 'Volatility 75 Index', 'Volatility 100 Index',
               'Volatility 10 (1s) Index', 'Volatility 25 (1s) Index', 'Volatility 50 (1s) Index', 'Volatility 75 (1s) Index',
               'Volatility 100 (1s) Index'}
    name = "Synthetic Market"
    symbol = SyntheticSymbol
