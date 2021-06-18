import requests
import pandas as pd
import argparse
import datetime
import warnings
from pathlib import Path
import yaml

warnings.filterwarnings("ignore")


class currency:
    """
    Currency object to get the best 
    buy and sell calls for a currency couple.
    """
    def __init__(self, operation, base):
        self.operation = operation
        self.base = base

    def getFromSource1(self):
        """
        Source: fawazahmed0
        Returns: DF with source, date and rates
        """
        url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{self.base}.json'
        print(f"Fetching data from {url}")
        resopnse = requests.get(url)
        if resopnse.status_code != 200:
            print(f'Failed\n\nResponse Code: {resopnse.status_code}')
            return pd.DataFrame({'date': [], 'rates': [], 'source': []})
        df = pd.DataFrame(resopnse.json())
        df = df.rename({self.base: 'rates'}, axis=1)
        df.index = df.index.str.upper()
        df['source'] = 'fawazahmed0'
        return df[['date', 'rates',
                   'source']].rename_axis('quote').reset_index()

    def getFromSource2(self):
        """
        Source: frankfurter
        Returns: DF with source, date and rates
        """
        url = f'https://api.frankfurter.app/latest?from={self.base}'
        print(f"Fetching data from {url}")
        try:
            resopnse = requests.get(url)
        except Exception as e:
            return pd.DataFrame({'date': [], 'rates': [], 'source': []})
        if resopnse.status_code != 200:
            print(f'Failed\n\nResponse Code: {resopnse.status_code}')
            return pd.DataFrame({'date': [], 'rates': [], 'source': []})
        df = pd.DataFrame(resopnse.json())
        df['source'] = 'frankfurter'
        return df[['date', 'rates',
                   'source']].rename_axis('quote').reset_index()

    def compareRates(self):
        """
        Pulls data from all the sources and selects based on the operation
        Returns: DF with best rates 
        Scalability: 
        To add more sources add 
        def getFromSource3()
        and add 
        df3 = self.getFromSource3()
        """
        df1 = self.getFromSource1()
        df2 = self.getFromSource2()
        df = pd.concat([df1, df2]).reset_index(drop=True)
        if self.operation == 'sell':
            idx = df.groupby(['quote'])['rates'].transform(max) == df['rates']
        else:
            idx = df.groupby(['quote'])['rates'].transform(min) == df['rates']
        df = df[idx]
        df['Operation'] = self.operation.capitalize()
        df['Base Currency'] = self.base.upper()
        return df[idx].reset_index(drop=True)

    def storeData(self, df):
        """
        Takes the final input and saves in the output_path
        This can later be updated to save the output in any database. With appropriate connection details passed to it.
        """
        dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = "../data"
        fname = f'{output_path}/bestrate_{self.operation}_{self.base}_{dt}.csv'
        print(f"Output is saved here: {fname}")
        Path(output_path).mkdir(parents=True, exist_ok=True)
        df.columns = df.columns.str.capitalize()
        df.to_csv(fname, index=False)
        return fname

    def getBestRate(self):
        df = self.compareRates()
        self.storeData(df)

if __name__ == '__main__':
    # capturing all valid currencies
    with open('config.yaml') as f:
        try:
            config_dict = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    my_parser = argparse.ArgumentParser()

    my_parser.add_argument('-s', '--sell',
                           dest='sell',
                           action='store_true',
                           default=False)
    my_parser.add_argument('-b', '--buy',
                           dest='buy',
                           action='store_true',
                           default=False,
                           help='Set a switch to true')
    my_parser.add_argument('base',
                           action='store',
                           nargs=1,
                           choices=config_dict['valid_currencies'],
                           type=str.upper,
                           help='Enter base currency from the valid currency codes')

    args = my_parser.parse_args()
    base = args.base[0].lower()
    if args.buy:
        print(f"Finding best buy value for {base}")
        currency_obj = currency('buy', base)
        currency_obj.getBestRate()
    if args.sell:
        print(f"Finding best sell value for {base}")
        currency_obj = currency('sell', base)
        currency_obj.getBestRate()

