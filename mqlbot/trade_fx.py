from concurrent.futures import ThreadPoolExecutor

import MetaTrader5 as mt5

from finger_trap import FingerTrap
from account import Account
from mqltrader import MqlTrader

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

symbols = [pairs, [trader for i in range(len(pairs))]]

with ThreadPoolExecutor(max_workers=len(pairs)) as executor:
    executor.map(FingerTrap, *symbols)
