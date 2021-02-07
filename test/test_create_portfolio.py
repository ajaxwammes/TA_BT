"""
Created on Sun Dec 13 23:07:01 2020
@author: mart.vos

To dos:
- What if there is extreme volatility, then no portfolio can be made?
- Introduce a measure to do overall risk rebalancing (again)
#TODO
- Set aside small amount to be able to pay ourselves the monthly fee, without having to make (extra) trades
    - First talk to custodian

Input:
    1. Sustainable categories
    2. Customer ID
    3. Amount of money investing
    4. Risk level
    5. Environment of all products
    
Output:
    1. Updated portfolio
    2. Customer ID
"""
import unittest

import pandas as pd
pd.options.mode.chained_assignment = None
try:
    from services.create_portfolio import PortfolioCreator
except ModuleNotFoundError as ex:
    import sys
    sys.path.append('./')
    from services.create_portfolio import PortfolioCreator

desired_width = 320
pd.set_option('display.max_rows', None)
#pd.set_option('display.width', desired_width)

class TestPortfolioCreator(unittest.TestCase):

    def setUp(self) -> None:
        self.all_products = pd.read_csv('./data/Portfolio2.csv')

        self.choices = [
            'Renewable energy',
        #    'Clean water and oceans',
             'Circular economy',
             'Transportation of the future',
            'Energy-saving technology',
             'Plant-based food'
        ]

        self.environment = pd.read_feather('./data/environment_2020_12_19.feather')
        self.fresh_environment = self.all_products[self.all_products.Industry.isin(self.choices)]

        self.customerID = 1002
        self.risk_level = 2
        self.money_in_portfolio = 50000


    # def test_split(self):
    #     pc_obj = PortfolioCreator(self.environment)
    #     result = pc_obj.run(money_in_portfolio=self.money_in_portfolio, risk_level=self.risk_level, all_products=self.all_products).reset_index(drop=True)
    #     true_output = pd.read_csv('./data/post_creation.csv')
    #     assert None == pd.testing.assert_frame_equal(result,true_output)

    def test_actual(self):
        pc_obj = PortfolioCreator(self.fresh_environment)
        result = pc_obj.run(money_in_portfolio=self.money_in_portfolio, risk_level=self.risk_level, all_products=self.all_products).reset_index(drop=True)
        print(result)
        print()


if __name__ == '__main__':
    unittest.main()