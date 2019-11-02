"""
This top-level function can be used to balance a default portfolio
from the command line. Use this function only if the package has 
been installed correctly

Place your private portfolio in the directory "resources/private_portfolio.txt"
Then, in the command line, run

> python balance_portfolio.py 1000

where 1000 is the amount (in USD) that you want to invest
"""

import argparse
import os
import glob

from portbalance import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cash", help="Cash to invest", type=float
    )
    parser.add_argument(
        "--portfolio", help="Path to a portfolio", type=str
    )
    parser.add_argument(
        "--allocation", help="Path to a portfolio", type=str
    )

    args = parser.parse_args()

    if not args.portfolio:
        all_paths = sorted(
            glob.glob(os.path.join("resources", "*.txt"))
        )

        if len(all_paths) == 0:
            raise Exception(
                'No user portfolios found. Create a portfolio with the \
				format "name.txt" and place it in the "resources" directory'
            )

        port_names = [
            os.path.os.path.basename(item)
            for item in all_paths
        ]

        path_dict = dict(zip(port_names, all_paths))

        if "private_portfolio.txt" in port_names:
            portfolio_path = path_dict[
                "private_portfolio.txt"
            ]
        elif "sample_portfolio.txt" in port_names:
            portfolio_path = path_dict[
                "sample_portfolio.txt"
            ]
        else:
            portfolio_path = all_paths[0]

    else:

        portfolio_path = args.portfolio

    if not args.allocation:
        allocation = get_strategy(
            "Bogleheads", stock_ratio=1.0
        )
    else:
        allocation = get_strategy(
        	args.allocation, stock_ratio=1.0
        )

    portfolio = Portfolio(portfolio_path)

    print(
        "\nNet return on principal:",
        portfolio.calculate_performance(),
        "\n",
    )

    ### Run gradient descent for a specified budget
    (
        my_buys,
        drift_final,
        leftover_cash,
    ) = portfolio.find_investing_strategy(
        args.cash, allocation
    )

    ### Print output
    print("Investing strategy:")
    for key in my_buys:
        print(key, ":", my_buys[key])

    print("\nResidual balance: ", leftover_cash)
    print(
        "Residual drift: ",
        str(100 * drift_final),
        "%",
        "\n",
    )


# Python 2 only
if __name__ == "__main__":
    main()
