import requests
import pandas as pd
import argparse
import datetime
import warnings
from pathlib import Path

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
        resopnse = requests.get(url)
        if resopnse.status_code != 200:
            print(f'Failed\n\nResponse Code: {resopnse.status_code}')
            return
        df = pd.DataFrame(resopnse.json())
        df = df.rename({'eur': 'rates'}, axis=1)
        df.index = df.index.str.upper()
        df['source'] = 'fawazahmed0'
        return df[['date', 'rates',
                   'source']].rename_axis('quote').reset_index()

    def getFromSource2(self):
        """
        Source: frankfurter
        """
        url = f'https://api.frankfurter.app/latest?from={self.base}'
        resopnse = requests.get(url)
        if resopnse.status_code != 200:
            print(f'Failed\n\nResponse Code: {resopnse.status_code}')
        df = pd.DataFrame(resopnse.json())
        df['source'] = 'frankfurter'
        return df[['date', 'rates',
                   'source']].rename_axis('quote').reset_index()

    def getBestRate(self):
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
        # df[df.quote.isin(common_curr)].to_csv('all.csv', index=False)
        if self.operation == 'sell':
            idx = df.groupby(['quote'])['rates'].transform(max) == df['rates']
        else:
            idx = df.groupby(['quote'])['rates'].transform(min) == df['rates']
        df = df[idx]
        df['Operation'] = self.operation
        df['Base Currency'] = self.base
        return df[idx].reset_index(drop=True)
        df[df.quote.isin(common_curr)].to_csv('buy.csv', index=False)
    def storeData(self):
        df = self.getBestRate()
        dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = "../data"
        fname = f'{output_path}/bestrate_{self.operation}_{dt}.csv'
        Path(output_path).mkdir(parents=True, exist_ok=True)
        df.to_csv(fname, index=False)
        return True



currency_obj = currency('sell', 'eur')
currency_obj.storeData()
currency_obj = currency('buy', 'eur')
currency_obj.storeData()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=(
        'pdf2pdfocr.py [https://github.com/LeoFCardoso/pdf2pdfocr] version %s (http://semver.org/lang/pt-BR/)'
        % VERSION),
                                     formatter_class=argparse.
                                     RawTextHelpFormatter)

# Output
"""
• Request Timestamp – timestamp when a request was submitted to CLI
• Trade Operation – a value of the second parameter
• Base Currency – a value of the first parameter
• Quote Currency – a value of quote currency retrieved from APIs
• Exchange Rate – the best exchange rate for the given currency couple
• Provider – the name of the provider that returned the best rate
"""

# Common Currencies
"""
common_curr = [
'AUD',
'BGN',
'BRL',
'CAD',
'CHF',
'CNY',
'CZK',
'DKK',
'GBP',
'HKD',
'HRK',
'HUF',
'IDR',
'ILS',
'INR',
'ISK',
'JPY',
'KRW',
'MXN',
'MYR',
'NOK',
'NZD',
'PHP',
'PLN',
'RON',
'RUB',
'SEK',
'SGD',
'THB',
'TRY',
'USD',
'ZAR']
"""