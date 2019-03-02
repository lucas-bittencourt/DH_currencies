import pandas as pd
import requests
import json
import sys
from pandas.io.json import json_normalize

class FixerIoCurrencies:

    API_KEY = 'a68384eaabca01c47b4d76e52e464067'
    BASE_URL = 'http://data.fixer.io/api/'
        
    def __init__(self, base):
        self.api_key  = '?access_key={}'.format(self.API_KEY)
        self.base_url = self.BASE_URL+'{}{}{}'
        self.base = '&base={}'.format(base)

    @classmethod
    def get_symbols(cls):
        url  = cls.BASE_URL+'{}{}'.format('symbols', '?access_key={}'.format(cls.API_KEY))
        try:
            response = requests.get(url)
            symbols_json = response.json()
            symbols_dict = dict(enumerate((line.strip() for line in symbols_json['symbols']),1))
            symbols_dict = {str(k):str(v) for k,v in symbols_dict.items()}
            return list(symbols_dict.items())
        except requests.ConnectionError as e:
            print(e)
            sys.exit(1)

    def get_latest_rate(self):
        url  = self.base_url.format('latest',self.api_key, self.base)
        try:
            response = requests.get(url)
            rates_json = response.json()
            return rates_json
        except requests.ConnectionError as e:
            print(e)
            sys.exit(1)
        
    def get_historical_rate(self, begin_date, end_date):
        range = pd.date_range(start=begin_date, end=end_date)
        rates_full = {'day':[]}
        for i in range:
            referenced_date = i.strftime('%Y-%m-%d')
            url  = self.base_url.format(referenced_date, self.api_key, self.base)
            try:
                response = requests.get(url)
                rates_json = response.json()
                rates_full["day"].append(rates_json)
            except requests.ConnectionError as e:
                print(e)
                sys.exit(1)
        results_json = json_normalize(rates_full['day'])
        df = results_json.drop(columns=['base','date','historical','success','timestamp'])
        df = df.rename(columns={col: col.split('.')[1] for col in df.columns})
        df = pd.DataFrame({'AVERAGE': df.mean(), 'MINIMUM': df.min(), 'MAXIMUM': df.max()})
        results = pd.DataFrame.to_json(df.T)
        return results

