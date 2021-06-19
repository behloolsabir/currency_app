import os
import pandas as pd
import datetime
from pathlib import Path

import os, sys

scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)


from src.trade import trade
from src.currency import currency

def compareRates(dfs, base, operation):
    """
    Pulls data from all the sources and selects based on the operation
    Returns: DF with best rates 
    Scalability: 
    To add more sources add 
    def getFromSource3()
    and add 
    df3 = self.getFromSource3()
    """
    df = pd.concat(dfs).reset_index(drop=True)
    if operation == 'sell':
        idx = df.groupby(['quote'])['rates'].transform(max) == df['rates']
    elif operation == 'buy':
        idx = df.groupby(['quote'])['rates'].transform(min) == df['rates']
    else:
        print("Invalid operation\nValid values: \n1. Buy\n2.Sell")
        os.exit(0)
    df = df[idx]
    # df['Operation'] = operation.capitalize()
    # df['Base Currency'] = base.upper()
    trades = []
    for idx, row in df.iterrows():
        trades.append(trade(currency(base), currency(row["quote"]), row["date"], row["source"], row["rates"], operation.capitalize()))
    return trades


def transact(providers, base, operation):
    dfs = []
    for provider in providers:
        dfs.append(provider.parseResponse(base))
    storeData(compareRates(dfs, base, operation), base, operation)


def storeData(trades, base, operation):
    """
    Takes the final input and saves in the output_path
    This can later be updated to save the output in any database. With appropriate connection details passed to it.
    """
    data = []
    for trade in trades:
        data.append([trade.base.name.upper(), trade.quote.name, trade.timestamp, trade.provider, trade.operation, trade.rate])

    df = pd.DataFrame(data, columns = ['Base', 'Quote', 'Date', 'Source', 'Operation', 'Rates'])

    dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = "../data"
    fname = f'{output_path}/bestrate_{operation}_{base}_{dt}.csv'
    print(f"Output is saved here: {fname}")
    Path(output_path).mkdir(parents=True, exist_ok=True)
    # df.columns = df.columns.str.capitalize()
    df.to_csv(fname, index=False)
    return fname
