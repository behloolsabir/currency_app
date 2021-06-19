import pandas as pd
import requests

class provider:
    """
    Provider object.
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def parseResponse(self, base):
        pass

    def getURL(self, base):
        pass

    def getData(self, base):

        # print(f"Fetching data from {url}")
        return requests.get(self.getURL(base))





class source1(provider):
    """
    Fawazahmed0 source.
    """
    def __init__(self):
        super().__init__(
            'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/'
        )

    def getURL(self, base):
        url = f'{self.base_url}{base}.json'
        return url

    def parseResponse(self, base):
        """
        Source: fawazahmed0
        Returns: DF with source, date and rates
        """
        resopnse = super().getData(base)

        if resopnse.status_code != 200:
            print(f'Failed\n\nResponse Code: {resopnse.status_code}')
            return pd.DataFrame({'date': [], 'rates': [], 'source': []})
        df = pd.DataFrame(resopnse.json())
        df = df.rename({base: 'rates'}, axis=1)
        df.index = df.index.str.upper()
        df['source'] = 'fawazahmed0'
        return df[['date', 'rates',
                   'source']].rename_axis('quote').reset_index()


class source2(provider):
    """
    Frankfurter source.
    """
    def __init__(self):
        super().__init__('https://api.frankfurter.app/latest?from=')

    def getURL(self, base):
        url = f"{self.base_url}{base}"
        return url

    def parseResponse(self, base):
        """
        Source: fawazahmed0
        Returns: DF with source, date and rates
        """
        try:
            resopnse = super().getData(base)
            # resopnse = requests.get(url)
        except Exception as e:
            return pd.DataFrame({'date': [], 'rates': [], 'source': []})
        if resopnse.status_code != 200:
            print(f'Failed\n\nResponse Code: {resopnse.status_code}')
            return pd.DataFrame({'date': [], 'rates': [], 'source': []})
        df = pd.DataFrame(resopnse.json())
        df['source'] = 'frankfurter'
        return df[['date', 'rates',
                   'source']].rename_axis('quote').reset_index()

