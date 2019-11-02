"""
Test the portbalance library

> python test_portbalance.py
"""
#!/usr/bin/env python
import os, glob
import unittest
from portbalance import Portfolio, get_current_prices

WORKING_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


class TestPortbalance(unittest.TestCase):
    """
    Tests portbalance
    """

    def test_api_key(self):
        """
        Test API key
        """
        key_path = glob.glob(
            os.path.join(
                WORKING_DIR,
                "portbalance",
                "assets",
                "keys.txt",
            )
        )

        assert (
            len(key_path) > 0
        ), "Please add a Tiingo API key at portbalance/assets/keys.txt"

    def test_portfolio(self):
        """
        Test the portfolio creation process
        """
        port = Portfolio(
            os.path.join(
                WORKING_DIR,
                "resources",
                "tiny_portfolio.txt",
            )
        )
        symbs = list(port.portfolio["Ticker"])

        assert set(symbs) == set(
            ["VTI", "SCHB"]
        ), "Portfolio creation not functioning"

    def test_queries(self):
        """
        Test looking up the value of a symbol
        """

        symb_vals = list(
            get_current_prices(["SCHB", "VTI"])
        )
        assert (
            symb_vals[0] > 0
        ), "Problem looking up pricing data"


if __name__ == "__main__":
    unittest.main()
