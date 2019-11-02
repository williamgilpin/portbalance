# portbalance

A lightweight python library for maintaining and monitoring a stock portfolio. This library
calculates an optimal investment given a finite budget and a target portfolio allocation, and it also allows measuring and plotting a portfolio's historical performance

This package was written by [William Gilpin](http://wgilpin.com)

## Installation

1. Download this repository and unzip the file.

2. Get API Access: Currently there are two APIs being used for stock data: Robinhood and Tiingo. To use the Tiingo API, sign up for a free account on the Tiingo website [here](https://api.tiingo.com/), which will come with an alphanumeric private key that is currently located [here](https://api.tiingo.com/account/token) if you are logged in. 

3. Paste your API key into a text file called `portbalance/assets/keys.txt` in the base directory **before installing**.
+ Note: if no `keys.txt` is found, then the library will fall back to using the Robinhood API, which has more limitations on pricing data.

4. Install using `setup.py`

	python setup.py install

5. Test the installation by running

	python tests/test_portbalance.py


Installation Notes: 

Only Python 3 is currently supported, due to limitations on API availability. The following packages are required and may be installed

+ numpy
+ matplotlib
+ pandas
+ pandas-datareader (for retrieving historical stock price data)

Additionally, you may consider also installing Jupyter in order to use the demos notebook


### Instructions

The general steps for using the tool are:

1. Enter your initial portfolio and holdings
2. Specify a target allocation among specific index funds, etc
3. Specify the amount of additional money that you want to invest
4. Run this code to calculate the best way to spend your money, in order to reduce the difference between your current allocations, and your target allocations

Place a text file containing your portfolio as a text file at `resources/private_portfolio.txt` Example files are included with the installation that show the correct formatting, but the general format of the portfolio file should be a CSV file with rows of the form `NAME, NUMSHARES, DATE`, e.g.

	VTI, 100, 12/2/2015,
	VXUS, 40, 1/1/1027,

After adding your portfolio, determine how much cash you want to use to re-balance. For example, for $1000, run the following in the command line

	> python balance_portfolio.py 1000

This will produce an output of the form

	Net return on principal: 0.5346585469336369 

	Investing strategy:
	VTI : 4
	VXUS : 79

	Residual balance:  114.63000000000648
	Residual drift:  34.01671763159314 % 

As a default, portbalance assumes a 100% stock Bogleheads portfolio (70% US domestic, 30% international index funds). To change the strategy to another one of the defaults, specify the strategy as an optional argument

	> python balance_portfolio.py 1000 --allocation Betterment2018

Which produces the output

	Net return on principal: 0.5346585469336369 

	Investing strategy:
	VEA : 60
	VXUS : 18
	VOE : 3
	VTV : 9

	Residual balance:  83.24000000000251
	Residual drift:  81.87810965693635 % 

The included allocation strategies are "Bogleheads", "Betterment2016", and "Betterment2018". Please note that these strategies (which are not necessarily accurate) are given for educational purposes only.

For details on specifying a custom allocation strategy, specifying a portfolio as a string, and plotting the performance over time, see the included demonstration notebook `demos/demo.ipynb` for a step-by-step walkthrough.




### Assumptions

In order to calculate a reasonable strategy, this code makes a few assumtions
+ No sells. This code finds the best way to invest additional money into your existing portfolio, but it will not include selling off current assests as part of its strategy
+ Greedy. Currently, the algorithm used by the app decides the best stock choice on a buy-by-buy basis. A more sophisticated algorithm would perform a full convex optimization given constraints on investment. However, this is asymptotically equivalent to the results of the greedy algorithm in the limit of large portfolios (>$5k or so)
+ Allocations. The "target portfolios" are based entirely on crowdsourced suggestions on public forums like the Bogleheads website. They are not necessarily accurate or recommended.


