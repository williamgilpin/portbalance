"""

A simple library for monitoring performance and re-balancing a stock portfolio

Provided tickers and allocations are for demonstrative and ecucational purposes, 
and are not recommendations.

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

def get_current_prices(symbols):
	"""
	A wrapper function for get_prices that gets the most recent price data
	available for a list of stocks
	"""

	price_df = get_prices(symbols, dt.datetime.now() - dt.timedelta(5), 
					dt.datetime.now())
	# Drop duplicate multiindices
	price_df = price_df[~price_df.index.get_level_values(0).duplicated(keep="last")]
	return price_df['close']

def get_strategy(name, stock_ratio=0.7):
	"""
	Given the string name of a strategy, return a portfolio allocation
	as a dict()

	name : "Betterment2016", "Bogleheads", "Betterment 2018"
	stock_ratio : float specifying the fraction stocks (vs. bonds)
	"""

	if name=="Bogleheads":
		strat = {
		'VTI' : stock_ratio*.35,
		'SCHB' : stock_ratio*.35, 
		'VXUS' : stock_ratio*.3,
		'BND' : (1-stock_ratio)*1.0,
				 }
	elif name=="Betterment2016":
		strat = {
		'VTI' : stock_ratio*0.087,
		'SCHB' : stock_ratio*0.087, 
		'VTV' : stock_ratio*0.178,
		'VOE' : stock_ratio*0.05,
		'VBR' : stock_ratio*0.05,
		'VEA' : stock_ratio*0.1025,
		'SCHF' : stock_ratio*0.1025,
		'VWO' : stock_ratio*0.03275,
		'IEMG' : stock_ratio*0.03275,
		'VXUS' : stock_ratio*0.2705,
		'BND' : (1-stock_ratio)*1.0,
				 }
	elif name=="Betterment2018":
		strat = {
		'VTI' : stock_ratio*0.1765,
		'SCHB' : stock_ratio*0.1765, 
		'VTV' : stock_ratio*0.094,
		'VOE' : stock_ratio*0.077,
		'VBR' : stock_ratio*0.065,
		'VEA' : stock_ratio*0.1295,
		'VWO' : stock_ratio*0.076,
		'VXUS' : stock_ratio*0.205,
		'BND' : (1-stock_ratio)*1.0,
				 }
	else:
		strat = dict()
		warnings.warn("No matching strategy found.")

	## Normalize to exactly one
	if np.isclose(sum(list(strat.values())), 1, .01):
		norm_val = 1.0/sum(strat.values())
		strat = {key: val*norm_val for key, val in strat.items() }

	return strat

class Portfolio(object):
	"""
	An object that stores a pandas DataFrame containing a list of stock
	purchases, times, and quantities given a string or a .csv file
	See example "sample_portfolio.txt"

	If purchase prices are not specified, they will be looked up during
	initialization.
	"""

	def __init__(self, data):
		"""
		data : a string or path to a file containing a portfolio
		"""
		self.portfolio = pd.read_csv(data, sep=',', 
			header=None, names=["Ticker", "NumShares", "Date", "BuyPrice"])
		
		self.current_values()
		self.fill_buy_values()
		
	def __getitem__(self, key):
		return self.portfolio[key]

	def __setitem__(self, key, item):
		self.portfolio[key] = item

	def current_values(self):
		"""
		Compute and update the current values of all tickers.
		This happens automatically during initialization, but 
		this function can be run again to update all prices
		"""
		# remove duplicate tickers
		symbs = list(set(np.array(self.portfolio['Ticker'])))

		df_curr = get_current_prices(symbs)
		symbs_prices = np.array(get_current_prices(symbs))
		
		# update portfolio with duplicates
		for symb, symb_price in zip(symbs, symbs_prices):
			where_same = np.where(self.portfolio["Ticker"]==symb)[0]
			self.portfolio.loc[where_same, "CurrentPrice"] = symb_price

		self.current_net_value = np.dot(self.portfolio['CurrentPrice'], self.portfolio['NumShares'])

		## Portfolio without duplicate buys
		portfolio_reduced = self.portfolio[['Ticker','NumShares','CurrentPrice']]
		portfolio_reduced = portfolio_reduced.groupby('Ticker').agg({ 'NumShares':np.sum, 'CurrentPrice': 'first'}).reset_index()
		self.portfolio_reduced = portfolio_reduced
	
	def fill_buy_values(self):
		"""
		Fill in any missing values in the "BuyPrice" column
		"""
		port = self.portfolio
		symbs = np.array(port['Ticker'])
		num_shares = np.array(port['NumShares'])
		buy_prices = np.array(port['BuyPrice'])
		dates = pd.to_datetime(port['Date'], format=' %m/%d/%Y')

		## Fill in missing price data
		missing_prices = list()
		for symb_m, date_m in zip(symbs[np.isnan(buy_prices)], dates[np.isnan(buy_prices)]):
			fill_df = get_prices(symb_m, date_m, date_m)
			missing_prices.append(fill_df['close'][0])
		buy_prices[np.isnan(buy_prices)] = missing_prices

		self.portfolio["BuyPrice"] = buy_prices
	
	def calculate_performance(self):
		"""
		Calculate the total simple return %
		"""
		self.current_values() ## update everything
		net_return = np.sum(self.current_net_value)/np.sum(self["BuyPrice"]*self["NumShares"]) - 1
		return net_return

	def find_investing_strategy(self, budget, my_strategy, verbose=False):
		"""
		Given a desired quantity to invest, calculate how much to buy of each
		stock in order to minimize remaining drift from the target allocation

		verbose : bool specifying where to return a full time series of the drift
			indexed by stock purchase number
		"""
		symbs_port = list(self.portfolio_reduced['Ticker'])
		symbs_strat = list(set(my_strategy.keys()))

		missing_symbs = [item for item in symbs_strat if item not in symbs_port]

		alloc_port = self.portfolio_reduced['NumShares']*self.portfolio_reduced['CurrentPrice']
		alloc_port /= np.sum(alloc_port)

		current_allocation = dict(zip(symbs_port, alloc_port))
		[current_allocation.update({item : 0.0}) for item in missing_symbs]

		# Get ordered list of current share counts
		df = self.portfolio_reduced
		num_shares = list()
		for key in symbs_strat:
			if key in list(df["Ticker"]):
				num_shares.append(int(df.loc[df["Ticker"]==key]["NumShares"]))
			else:
				num_shares.append(0)
		num_shares = np.array(num_shares)

		curr_prices = np.array(get_current_prices(symbs_strat))
		curr_alloc = np.array([current_allocation[key] for key in symbs_strat])
		sim_alloc = np.copy(curr_alloc)
		sim_shares = np.copy(num_shares)
		target_alloc = np.array([my_strategy[key] for key in symbs_strat])

		buy_series = list()
		cost_series = [0.0]
		drift_series = list()
		total_cost = 0

		while budget>total_cost:
			drift = sim_alloc - target_alloc
			net_drift = np.sum(np.abs(drift))
			rel_drift = (drift*curr_prices)/curr_prices
			ordering = np.argsort(rel_drift)
			buy_index = ordering[0]
			
			total_cost += curr_prices[buy_index]

			sim_shares[buy_index] += 1
			sim_alloc = (sim_shares*curr_prices)/(sim_shares.dot(curr_prices))

			buy_series.append(buy_index)
			cost_series.append(total_cost)
			drift_series.append(net_drift)
		cost_series = np.array(cost_series)[:-1]
		buy_series = np.array(buy_series)[:-1]
		drift_series = np.array(drift_series)[:-1]


		inds, cts = np.unique(buy_series, return_counts=True)
		buy_strat = dict()
		for ind, ct in zip(inds,cts):
			buy_strat.update({str(symbs_strat[ind]) : ct})
		residual_budget = budget-cost_series[-1]
		residual_drift = drift_series[-1]

		if verbose:
			return buy_strat, drift_series, budget-cost_series
		else:
			return buy_strat, residual_drift, residual_budget



