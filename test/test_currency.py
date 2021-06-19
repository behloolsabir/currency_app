import unittest

import pandas as pd

import os, sys

sys.path.insert(0, os.path.abspath("."))

# scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
# os.chdir(scriptPath)
# myPath = os.path.dirname(os.path.abspath(__file__))
# print(myPath)
# sys.path.insert(0, myPath + '/../src')

from src import utils
from src.provider import source1, source2

# https://stackoverflow.com/questions/12813633/how-to-assert-two-list-contain-the-same-elements-in-python

class TestCurrency(unittest.TestCase):
    def test_getFromSource(self):
        base = 'usd'
        providers = [source1(), source2()]
        for provider in providers:
            got = provider.parseResponse(base)
            self.assertCountEqual(['quote', 'date', 'rates', 'source'],
                                  got.columns.tolist())
            self.assertGreaterEqual(got.shape[0], 0)

    def test_buy_compareRates(self):
        base = 'base_curr'
        operation = 'buy'
        # currency_obj = currency.currency(operation, base)

        df1 = pd.DataFrame({
            'quote': ['curr_a', 'curr_b', 'curr_c'],
            'date': ['1234', '1234', '1234'],
            'rates': [1, 2, 3],
            'source': ["SourceA", "SourceA", "SourceA"]
        })
        df2 = pd.DataFrame({
            'quote': ['curr_a', 'curr_b', 'curr_c', 'curr_d'],
            'date': ['1234', '1234', '1234', '1234'],
            'rates': [3, 2, 1, 0],
            'source': ["SourceB", "SourceB", "SourceB", "SourceB"]
        })

        got = utils.compareRates([df1, df2], base, operation)

        for trade in got:
            if trade.quote.name == 'curr_a':
                self.assertEqual('SourceA', trade.provider)
            elif trade.quote.name == 'curr_b':
                try:
                    self.assertEqual('SourceA', trade.provider)
                except AssertionError:
                    self.assertEqual('SourceB', trade.provider)
            elif trade.quote.name == 'curr_c':
                self.assertEqual('SourceB', trade.provider)
            elif trade.quote.name == 'curr_a':
                self.assertEqual('SourceB', trade.provider)

    def test_sell_compareRates(self):
        base = 'base_curr'
        operation = 'sell'
        # currency_obj = currency.currency(operation, base)

        df1 = pd.DataFrame({
            'quote': ['curr_a', 'curr_b', 'curr_c'],
            'date': ['1234', '1234', '1234'],
            'rates': [1, 2, 3],
            'source': ["SourceA", "SourceA", "SourceA"]
        })
        df2 = pd.DataFrame({
            'quote': ['curr_a', 'curr_b', 'curr_c', 'curr_d'],
            'date': ['1234', '1234', '1234', '1234'],
            'rates': [3, 2, 1, 0],
            'source': ["SourceB", "SourceB", "SourceB", "SourceB"]
        })

        got = utils.compareRates([df1, df2], base, operation)

        for trade in got:
            if trade.quote.name == 'curr_a':
                self.assertEqual('SourceB', trade.provider)
            elif trade.quote.name == 'curr_b':
                try:
                    self.assertEqual('SourceA', trade.provider)
                except AssertionError:
                    self.assertEqual('SourceB', trade.provider)
            elif trade.quote.name == 'curr_c':
                self.assertEqual('SourceA', trade.provider)
            elif trade.quote.name == 'curr_a':
                self.assertEqual('SourceB', trade.provider)


if __name__ == '__main__':
    unittest.main()
