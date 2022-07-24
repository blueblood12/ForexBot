import MetaTrader5 as mt5

from finger_trap import FingerTrap
from account import Account
from mqltrader import MqlTrader
from executor import Executor

pairs = ['AUDCAD', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'CADCHF', 'CADJPY', 'CHFJPY','GBPCAD', 'EURUSD',
           'GBPAUD', 'GBPCHF', 'GBPJPY', 'GBPUSD','NZDCAD', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY']

if not mt5.initialize():
    print("unable to initialize terminal")
    quit()

account = Account(login=5050656, password="nwa0#anaEze", server="Deriv-Demo")

if not account.connected:
    print("Unable to connect to account")
    quit()

trader = MqlTrader(account=account)

symbols = [{"symbol": pair, "trader": trader} for pair in pairs]
exe = Executor()
exe.add_workers(strategy=FingerTrap, kwargs=symbols)
exe.execute()
