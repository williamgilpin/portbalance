"""

A simple library for monitoring performance and re-balancing a stock portfolio

Some aspects of the stock prices method are based on 
https://pythonprogramming.net/getting-stock-prices-python-programming-for-finance/

"""


import warnings, glob, os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# pd.core.common.is_list_like = pd.api.types.is_list_like  # can remove this when v0.7 of pdr is available
import pandas_datareader.data as web
import datetime as dt


## Determine which api to use to retrieve price data, since these are somewhat unstable
## TODO: Add tests to see which APIs are working
if len(glob.glob('keys.txt'))>0:
	api_key = str(np.loadtxt('keys.txt', dtype='str'))
	api_flag = "tiingo"
else:
	api_flag = 'rh'
	warnings.warn("""Tiingo API key not found, falling back to robinhood API. To fix, 
		sign up for an API key at the Tiingo website, then store it in a file "key.txt" 
		somewhere in the home directory""")


def get_prices(symbols, start, end):
    """
    A wrapper function for getting the prices of a
    list of ticker symbols
    
    symbols : list of strings
    start : datetime.datetime() of starting day
    end : datetime.datetime() of starting day
    """
    if api_flag=="tiingo":
        out_df = web.get_data_tiingo(symbols, start, end, api_key=api_key)
        # out_df = out_df.rename(columns={"close":"unAdjClose"})
        out_df = out_df.rename(columns={"adjClose":"close", "close":"unAdjClose"})
    elif api_flag=='rh':
        out_df = web.DataReader(symbols, 'robinhood', start, end) 
        out_df = out_df.rename(columns={'close_price':'close'})
    else:
        warnings.warn("No suitable financial data API found during import.")
    
    return out_df




class Portfolio(object):
	"""
	A portfolio class.
	"""

	def __init__(self, data):
		"""
		data : a string or path to a file containing a portfolio
		"""
		self.portfolio = pd.read_csv(data, sep=',', 
			header=None, names=["Ticker", "NumShares", "Date", "Price"])
		self.fill_buy_values()
	
	def fill_buy_values(self):
		"""
		Fill in any missing values in the "Price" column
		"""
		port = self.portfolio
		symbs = np.array(port['Ticker'])
		num_shares = np.array(port['NumShares'])
		buy_prices = np.array(port['Price'])
		dates = pd.to_datetime(port['Date'], format=' %m/%d/%Y')

		## Fill in missing price data
		missing_prices = list()
		for symb_m, date_m in zip(symbs[np.isnan(buy_prices)], dates[np.isnan(buy_prices)]):
		    fill_df = get_prices(symb_m, date_m, date_m)
		    missing_prices.append(fill_df['close'][0])
		buy_prices[np.isnan(buy_prices)] = missing_prices

		self.portfolio["Price"] = buy_prices
	
	def current_value(self):
		"""
		Compute the current value
		"""
		symbs = np.array(self.portfolio['Ticker'])
		df_curr = get_prices(symbs, dt.datetime.now() - dt.timedelta(1), 
			dt.datetime.now() - dt.timedelta(1))
		return df_curr['close']

	def assign_allocation(self):
		# self.target_alloc = 
		pass

	def calculate_performance(self):
		pass



# 	def recommend_rebalance(cash):
# 		"""
# 		cash : float specifying the amount of money with which to rebalance
# 		"""
# 		pass