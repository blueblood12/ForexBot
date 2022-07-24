import MetaTrader5 as mt5

from finger_trap import FingerTrap
from account import Account
from mqltrader import MqlTrader
from executor import Executor

indices = ['Volatility 10 Index', 'Volatility 25 Index', 'Volatility 50 Index', 'Volatility 75 Index', 'Volatility 100 Index',
           'Volatility 10 (1s) Index', 'Volatility 25 (1s) Index', 'Volatility 50 (1s) Index', 'Volatility 75 (1s) Index',
           'Volatility 100 (1s) Index']

if not mt5.initialize():
    print("unable to initialize terminal")
    quit()

account = Account(login=5054652, password="nwa0#anaEze", server="Deriv-Demo", market='synthetic')

if not account.connected:
    print("Unable to connect to account")
    quit()

trader = MqlTrader(account=account)

symbols = [{"symbol": index, "trader": trader} for index in indices]
exe = Executor()
exe.add_workers(strategy=FingerTrap, kwargs=symbols)
exe.execute()
