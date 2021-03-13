"""
Created on Sat Jan 23 11:19:14 2021
@author: mart.vos

Impact calculation

"""

import pandas as pd
try:
    from experimental.calculate_impact import ImpactCalculator
except ModuleNotFoundError as ex:
    import sys
    sys.path.append('../test/')
    from experimental.calculate_impact import ImpactCalculator

pd.options.mode.chained_assignment = None
#desired_width = 320
#pd.set_option('display.width', desired_width)

if __name__ == "__main__":
    #TODO need 2 scripts for impact? 1 for projection and 1 for live updates?
    portfolio_creation_date = (2021,1,1)
    begin_portfolio = pd.read_csv('./data/post_creation.csv')

    environment = begin_portfolio

    ba_obj = ImpactCalculator(environment)

    result = ba_obj.run(begin_portfolio=begin_portfolio)

    print(result)
