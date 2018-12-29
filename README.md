# portbalance

A lightweight python library for maintaining and monitoring a stock portfolio. This library
calculates an optimal investment given a finite budget and a target portfolio allocation.

### Dependencies

Please install
+ numpy
+ matplotlib
+ pandas
+ pandas-datareader (for retrieving historical stock price data)
+ jupyter notebook (for using the tutorial notebook)

### API Access

Currently there are two APIs being used for stock data: Robinhood and Tiingo. To use the Tiingo API, sign up for a free account on the Tiingo website, which will come with an alphanumeric private key. Put this key into a text file called `keys.txt` in the base directory.
If no `keys.txt` is found, then the library will fall back to using the Robinhood API, which has more limitations on pricing data.

### Instructions

See `demo.ipynb` for a step-by-step walkthrough. Your portfolio can be entered as a string, or specified as a CSV file (see `sample_portfolio.txt`). The general steps are:

+ Enter your initial portfolio and holdings
+ Specify a target allocation among specific index funds, etc
+ Specify the amount of additional money that you want to invest
+ The code will calculate the best way to spend your money to reduce the difference vbetween your current allocations, and your target allocations

Demonstrative investment portfolio strategies are contained in the function `get_strategy`. These estimates (which are not necessarily accurate) are given for educational purposes only.


### Assumptions

In order to calculate a reasonable strategy, this code makes a few assumtions
+ No sells. This code finds the best way to invest additional money into your existing portfolio, but it will not include selling off current assests as part of its strategy
+ Greedy. Currently, the algorithm used by the app decides the best stock choice on a buy-by-buy basis. A more sophisticated algorithm would perform a full convex optimization given constraints on investment. However, this is asymptotically equivalent to the results of the greedy algorithm in the limit of large portfolios (>$5k or so)
+ Allocations. The "target portfolios" are based entirely on crowdsourced suggestions on public forums like the Bogleheads website. Much better long-term performance likely may be achieved by using a unique portfolio strategy based on professional and individualized research.


