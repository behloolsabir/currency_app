import unittest

import pandas as pd

import os, sys

sys.path.insert(0, os.path.abspath("."))

from src import currency

# https://stackoverflow.com/questions/12813633/how-to-assert-two-list-contain-the-same-elements-in-python

class TestCurrency(unittest.TestCase):
    def test_getFromSource(self):
        base = 'usd'
        operation = 'buy'
        currency_obj = currency.currency(operation, base)

        got = currency_obj.getFromSource1()
        self.assertCountEqual(['quote', 'date', 'rates', 'source'],
                              got.columns.tolist())
        self.assertGreaterEqual(got.shape[0], 0)

        got = currency_obj.getFromSource2()
        self.assertCountEqual(['quote', 'date', 'rates', 'source'],
                              got.columns.tolist())
        self.assertGreaterEqual(got.shape[0], 0)

    def test_buy_compareRates(self):
        base = 'usd'
        operation = 'buy'
        currency_obj = currency.currency(operation, base)
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

        got = currency_obj.compareRates(df1, df2)
        self.assertCountEqual(
            ['quote', 'date', 'rates', 'source', 'Operation', 'Base Currency'],
            got.columns.tolist())
        curr_a = got[got.quote == 'curr_a']['source'].values.tolist()
        curr_b = got[got.quote == 'curr_b']['source'].values.tolist()
        curr_c = got[got.quote == 'curr_c']['source'].values.tolist()
        curr_d = got[got.quote == 'curr_d']['source'].values.tolist()

        self.assertCountEqual(['SourceA'], curr_a)
        self.assertCountEqual(['SourceA', 'SourceB'], curr_b)
        self.assertCountEqual(['SourceB'], curr_c)
        self.assertCountEqual(['SourceB'], curr_d)

    def test_sell_compareRates(self):
        base = 'usd'
        operation = 'sell'
        currency_obj = currency.currency(operation, base)
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

        got = currency_obj.compareRates(df1, df2)
        self.assertCountEqual(
            ['quote', 'date', 'rates', 'source', 'Operation', 'Base Currency'],
            got.columns.tolist())
        curr_a = got[got.quote == 'curr_a']['source'].values.tolist()
        curr_b = got[got.quote == 'curr_b']['source'].values.tolist()
        curr_c = got[got.quote == 'curr_c']['source'].values.tolist()
        curr_d = got[got.quote == 'curr_d']['source'].values.tolist()

        self.assertCountEqual(['SourceB'], curr_a)
        self.assertCountEqual(['SourceA', 'SourceB'], curr_b)
        self.assertCountEqual(['SourceA'], curr_c)
        self.assertCountEqual(['SourceB'], curr_d)

if __name__ == "__main__":
    unittest.main()