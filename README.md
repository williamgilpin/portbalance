# portbalance


Calculation of optimal investment given a finite budget and a target portfolio allocation.

### Dependencies

Please install
+ numpy
+ matplotlib
+ jupyter notebook (for using the tutorial notebook)
+ pandas (for aquiring financial data)

### Instructions

Decide on an investment portfolio strategy. Estimates (not necessarily accurate) of a few common portfolio strategies are given for educational purposes only.

+ Enter your initial portfolio and holdings
+ Specify the amount of additional money that you want to invest
+ The code will calculate the best way to spend your money to reduce the difference vbetween your current allocations, and your target allocations

### Assumptions

In order to calculate a reasonable strategy, this code makes a few assumtions
+ No sells. This code finds the best way to invest additional money into your existing portfolio, but it will not include selling off current assests as part of its strategy
+ Greedy. Currently, the algorithm used by the app decides the best stock choice on a buy-by-buy basis. A more sophisticated algorithm would perform a full convex optimization given constraints on investment. However, this is asymptotically equivalent to the results of the greedy algorithm in the limit of large portfolios (>$5k or so)
+ Allocations. The "target portfolios" are based entirely on crowdsourced suggestions on public forums like the Bogleheads website. Much better long-term performance likely may be achieved by using a unique portfolio strategy based on professional and individualized research.


