"""
Created on Mon Dec 14 11:07:14 2020
@author: mart.vos

Rebalancing portfolio

Input:
    1. Latest portfolio (from API)
    2. Customer ID
    
Output:
    1. Updated portfolio
    2. Customer ID
"""

import pandas as pd
try:
    from services.rebalance import Rebalancer
except ModuleNotFoundError as ex:
    import sys
    sys.path.append('./')
    from services.rebalance import Rebalancer

pd.options.mode.chained_assignment = None
#desired_width = 320
#pd.set_option('display.width', desired_width)

if __name__ == "__main__":
    CustomerID = 1001
    begin_portfolio = pd.read_csv('./data/post_creation.csv')

    environment = begin_portfolio

    ba_obj = Rebalancer(environment)

    result = ba_obj.run(begin_portfolio=begin_portfolio)

    print(result)