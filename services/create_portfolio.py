"""
Created on Mon Dec 14 14:32:57 2020
@author: mart.vos

Create portfolio
"""

from futures3.thread import ThreadPoolExecutor
import random

import numpy as np
import pandas as pd

from services.configs import risk_thresholds_levels as RTL
from services.utils.utils import analyst_ratings
from services.utils.utils import risk


class PortfolioCreator:

    def __init__(self,environment):
        self.environment = environment
    
    def total_portfolio_risk(self):
        self.environment['Weighted_risk'] = (self.environment['Value_per_stock']/sum(self.environment['Value_per_stock']))*self.environment['Risk']*len(self.environment)
        total_portfolio_risk = sum(self.environment['Weighted_risk'])/len(self.environment)
        return total_portfolio_risk

    def analyst_ratings(self):
        if 'Analyst_rating' not in self.environment.columns:
            self.environment = analyst_ratings(self.environment)

    def capital_check(self,begin_portfolio):
        portfolio_value_start = round(sum(begin_portfolio['Value_per_stock']),2)
        portfolio_value_now = round(sum(self.environment['Value_per_stock']),2)
        rest_value = portfolio_value_start - portfolio_value_now
        if rest_value != 0:
            cond=self.environment['Value_per_stock'] > 10
            x = np.where(cond)
            x = np.array(x).tolist()[0]
            i = random.choice(x)
            self.environment.Value_per_stock.iloc[i] = self.environment.Value_per_stock.iloc[i] + rest_value
        else:
            print('Risk Check Complete!')

    def get_trades(self,begin_portfolio):
        self.environment['trades'] = round(self.environment['Value_per_stock'] - begin_portfolio['Value_per_stock'],2)

    def portfolio_length(self,money_in_portfolio):
        portfolio_length = round(np.clip(money_in_portfolio/RTL.portfolio_length_variable,RTL.min_portfolio_length,RTL.max_portfolio_length))
        return portfolio_length

    def portfolio_lmh(self,money_in_portfolio,risk_level):
        """calculate whether the risk level is low, medium or high and allocate number of
            low, medium and high stock to selected risk level
        """
        conditions = [
            (self.environment['Risk'] <= RTL.risk_threshold_l),
            (self.environment['Risk'] > RTL.risk_threshold_l) & (self.environment['Risk'] <= RTL.risk_threshold_m),
            (self.environment['Risk'] > RTL.risk_threshold_m) & (self.environment['Risk'] <= RTL.risk_threshold_h),
            (self.environment['Risk'] > RTL.risk_threshold_h)
            ]
        
        values = ['Low', 'Medium', 'High', 'Unacceptable']
        self.environment['Tier'] = np.select(conditions, values)
        low_risk = self.environment.loc[self.environment['Tier'] == 'Low']
        medium_risk = self.environment.loc[self.environment['Tier'] == 'Medium']
        high_risk = self.environment.loc[self.environment['Tier'] == 'High']
        len_low_risk = round(self.portfolio_length(money_in_portfolio)*RTL.risk_based_allocation[risk_level][0])
        len_med_risk = round(self.portfolio_length(money_in_portfolio)*RTL.risk_based_allocation[risk_level][1])
        len_high_risk = round(self.portfolio_length(money_in_portfolio)*RTL.risk_based_allocation[risk_level][2])
        
        elements_low = low_risk.sort_values('Risk',ascending=True).head(len_low_risk)
        elements_med = medium_risk.sort_values('Risk',ascending=True).head(len_med_risk)
        elements_high = high_risk.sort_values('Risk',ascending=True).head(len_high_risk)
        
        frames = [elements_low, elements_med, elements_high]
        self.environment = pd.concat(frames)

    def portfolio_lmh2(self,additional_prod,risk_level,money_in_portfolio):
        conditions = [
            (self.environment['Risk'] <= RTL.risk_threshold_l),
            (self.environment['Risk'] > RTL.risk_threshold_l) & (self.environment['Risk'] <= RTL.risk_threshold_m),
            (self.environment['Risk'] > RTL.risk_threshold_m) & (self.environment['Risk'] <= RTL.risk_threshold_h),
            (self.environment['Risk'] > RTL.risk_threshold_h)
            ]
        
        values = ['Low', 'Medium', 'High', 'Unacceptable']
        self.environment['Tier'] = np.select(conditions, values)
        low_risk = self.environment.loc[self.environment['Tier'] == 'Low']
        medium_risk = self.environment.loc[self.environment['Tier'] == 'Medium']
        high_risk = self.environment.loc[self.environment['Tier'] == 'High']
        
        #get new risk level 1:
        risk_level2 = self.risklvl_lmh2(risk_level,money_in_portfolio)
        len_low_risk = round(additional_prod*RTL.risk_based_allocation[risk_level2][0])  
        len_med_risk = round(additional_prod*RTL.risk_based_allocation[risk_level2][1])
        len_high_risk = round(additional_prod*RTL.risk_based_allocation[risk_level2][2])
        
        elements_low = low_risk.sort_values('Risk',ascending=True).head(len_low_risk)
        elements_med = medium_risk.sort_values('Risk',ascending=True).head(len_med_risk)
        elements_high = high_risk.sort_values('Risk',ascending=True).head(len_high_risk)
        
        frames = [elements_low, elements_med, elements_high]
        self.environment = pd.concat(frames)

    def risklvl_lmh2(self,risk_level,money_in_portfolio):
        should_be_risk_total = RTL.risk_lvl[risk_level]
        risk_port1 = sum(self.environment['Risk'])/len(self.environment)
        lenght_total = self.portfolio_length(money_in_portfolio)
        lenght_port1 = len(self.environment)
        lenght_port2 = lenght_total - len(self.environment)
        weight_port1 = lenght_port1 / lenght_total
        weight_port2 = lenght_port2 / lenght_total
        calc = (1/weight_port2) * (should_be_risk_total - (risk_port1*weight_port1))
        res_key, res_val = min(RTL.risk_lvl.items(), key=lambda x: abs(calc - x[1]))
        return res_key

    def add_stocks(self,all_products,money_in_portfolio,risk_level):
        original_environment = self.environment.copy()
        additional_prod = self.portfolio_length(money_in_portfolio) - len(self.environment)
        cond = all_products['Ticker'].isin(self.environment['Ticker'])
        self.environment = all_products.drop(all_products[cond].index)
        self.analyst_ratings()
        self.risk_clean()
        self.portfolio_lmh2(additional_prod,risk_level,money_in_portfolio)
        frames = [original_environment, self.environment]
        self.environment = pd.concat(frames)
        self.environment = self.environment.sort_values('Risk')

    def risk_clean(self):
        companylist = list(self.environment['Ticker'])
        self.value_risk = []
        with ThreadPoolExecutor(max_workers=10) as executer:
            Value_risk = executer.map(risk, companylist)
            for Value_risk in Value_risk:
                self.value_risk.append(Value_risk)
        self.environment['Risk'] = self.value_risk
        self.environment = self.environment.dropna()
        self.environment = self.environment[pd.to_numeric(self.environment['Risk'], errors='coerce').notnull()]

    def value_per_stock(self,money_in_portfolio):
        value_per_stock = round(money_in_portfolio / len(self.environment),2)
        cent_check = round(money_in_portfolio - value_per_stock*len(self.environment),2)
        self.environment['Value_per_stock'] = value_per_stock
        self.environment.Value_per_stock.iloc[-1] = self.environment.Value_per_stock.iloc[-1] + cent_check
        print('Portfolio is made!')

    def portfolio_check(self,money_in_portfolio,risk_level,all_products):
        if len(self.environment) <= self.portfolio_length(money_in_portfolio)*RTL.rebalance_threshold:
            print('Warning: not enough financial products for capital, adding:',self.portfolio_length(money_in_portfolio) - len(self.environment))
            self.add_stocks(all_products,money_in_portfolio,risk_level)
        else:
            print('Financial products check: DONE BRO')


    def run(self, money_in_portfolio, risk_level, all_products):
        self.analyst_ratings()
        self.risk_clean()
        self.portfolio_lmh(money_in_portfolio,risk_level)
        self.portfolio_check(money_in_portfolio,risk_level,all_products)
        self.value_per_stock(money_in_portfolio)
        return self.environment
