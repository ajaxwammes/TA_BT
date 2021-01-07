"""
Created on Mon Dec 14 14:16:28 2020
@author: mart.vos

Deposit / Withdraw check

Input:
    1. Latest portfolio (from API)
    2. Customer ID
    3. Money delta (how much USD deposited / withdrawn)
    
Output:
    1. Updated portfolio
    2. Customer ID
"""

import pandas as pd
try:
    from services.withdraw_deposit import DepositWithdrawer
except ModuleNotFoundError as ex:
    import sys
    sys.path.append('./')
    from services.withdraw_deposit import DepositWithdrawer

#desired_width = 320
#pd.set_option('display.width', desired_width)

if __name__ == "__main__":
    #INPUT
    CustomerID = 1001
    money_delta = 100
    begin_portfolio = pd.read_csv('./data/post_creation.csv')

    dw_obj = DepositWithdrawer(environment_org=begin_portfolio)

    result = dw_obj.run(begin_portfolio=begin_portfolio,
               money_delta=money_delta)

    print(result)