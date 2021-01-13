"""
Created on Mon Dec 14 13:44:11 2020
@author: mart.vos

Risk thresholds and levels
"""

#percentages of low, medium and high financial products per risk level
risk_based_allocation = {0: (0.9,0.1,0), #very conservative
                         1: (0.8,0.1,0.1), #conservative
                         2: (0.7,0.2,0.1), #moderate
                         3: (0.6,0.2,0.2), #opportunistic
                         4: (0.5,0.3,0.2) #very opportunistic
                         }

#average risk levels for 3 type of stocks (LR = Low Risk)
LR=0.019
MR=0.0373
HR=0.0578

#average risk levels (should be)
risk_lvl = {0: (risk_based_allocation[0][0]*LR+risk_based_allocation[0][1]*MR+risk_based_allocation[0][2]*HR),  
            1: (risk_based_allocation[1][0]*LR+risk_based_allocation[1][1]*MR+risk_based_allocation[1][2]*HR),
            2: (risk_based_allocation[2][0]*LR+risk_based_allocation[2][1]*MR+risk_based_allocation[2][2]*HR),
            3: (risk_based_allocation[3][0]*LR+risk_based_allocation[3][1]*MR+risk_based_allocation[3][2]*HR),
            4: (risk_based_allocation[4][0]*LR+risk_based_allocation[4][1]*MR+risk_based_allocation[4][2]*HR)
            }

#thresholds for individual stock risk allocation into low, medium or high
risk_threshold_l = 0.033
risk_threshold_m = 0.048
risk_threshold_h = 0.084

#API call to get 100 day volatility
market_data_provider = 'yahoo'
lhs_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
rhs_url = '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&' \
          'modules=upgradeDowngradeHistory,recommendationTrend,' \
          'financialData,earningsHistory,earningsTrend,industryTrend&' \
          'corsDomain=finance.yahoo.com'

#risk calculation is done taking the average of n days of volatility
days_volatility = 100

#taking the trend of the last n days, to check for positive or negative trend
days_trend = 1400

#Volatility threshold
volatility_threshold = 100000

#mix/max portfolio length
min_portfolio_length = 30
max_portfolio_length = 40

#money in portfolio / portfolio_length_variable = no of stocks
portfolio_length_variable = 150

#if the no of stocks in less than % of what is should be: rebalance
rebalance_threshold = 0.9

#stocks with an analyst rating of < are prioritized
analyst_rating_threshold_prio = 2.7

# 1-analyst_rating_threshold_drop: % that will not be considered in portfolio creation, thus dropped before
analyst_rating_threshold_drop = 0.9

#when the reallocation ratio is < this, dont rebalance all, but only prioritzed
individual_rebalance_threshold = 0.1

#Reallocation amount / (Average value per stock * no_trades_variable) = no of trades
no_trades_variable = 0.19

#when an individual stock is worth > weigthed_risk_value, rebalance the stock
weigthed_risk_threshold = 1.4