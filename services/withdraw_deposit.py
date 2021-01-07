"""
Created on Mon Dec 14 14:31:39 2020
@author: mart.vos

Withdrawing or depositing
"""

import pandas as pd
import numpy as np
import random
from services.utils.utils import analyst_ratings
from services.configs import risk_thresholds_levels as RTL

class DepositWithdrawer:

    def __init__(self, environment_org):
        self.environment = environment_org
    
    def _individual_deposit_withdraw_check(self, begin_portfolio, money_delta):
        cond=self.environment['Weighted_allocation'] > RTL.weigthed_risk_threshold
        x = np.where(cond)
        x = np.array(x).tolist()[0]
        for i in x:
            self.environment.Value_per_stock.iloc[i] = round(self.environment.Value_per_stock.iloc[i] / self.environment.Weighted_allocation.iloc[i],2)
        
        #reallocate money from sold products and deposit/withdraw
        value_portfolio_start = round(sum(begin_portfolio['Value_per_stock']),2)
        value_portfolio_now = round(sum(self.environment['Value_per_stock']),2)
        amount_reallocation = round(value_portfolio_start - value_portfolio_now + money_delta,2)
        amount_reallocation_ratio = amount_reallocation / value_portfolio_now

        if value_portfolio_now - value_portfolio_start + money_delta == 0:
            print('Nothing to be reallocated')

        elif amount_reallocation_ratio > RTL.individual_rebalance_threshold or amount_reallocation_ratio < -RTL.individual_rebalance_threshold:
            amount_reallocation_ps = amount_reallocation / len(self.environment)
            self.environment['Value_per_stock'] = round(self.environment['Value_per_stock'] + amount_reallocation_ps,2)
        else:
            average_value_ps = value_portfolio_start / len(self.environment)
            no_of_trades2 = round(abs(amount_reallocation / (average_value_ps * RTL.no_trades_variable)))
            no_of_trades = np.clip(no_of_trades2, 1, round(len(self.environment) / 2))
            amount_reallocation_ps = amount_reallocation / round(no_of_trades)
            
            if amount_reallocation < 0:
                negative_list = self.environment['Value_per_stock'] > abs(amount_reallocation_ps)
                y = np.where(negative_list)
                y = np.array(y).tolist()[0]
                list1 = random.sample((y), no_of_trades)
            elif amount_reallocation > 0:
                self._analyst_ratings()
                list1 = self._list_incorp_analyst_ratings(no_of_trades)
            
            for j in list1:
                self.environment.Value_per_stock.iloc[j] = round(self.environment.Value_per_stock.iloc[j] + amount_reallocation_ps,2)

    def _list_incorp_analyst_ratings(self, no_of_trades):
        top=np.where([(self.environment['Analyst_rating']>0.1) & (self.environment['Analyst_rating']<RTL.analyst_rating_threshold_prio)])
        z = np.array(top).tolist()[1]
        
        if no_of_trades <= len(z):
            return z[:no_of_trades]
        if no_of_trades > len(z):
            remaining_values = no_of_trades - len(z)
            total_list = list(range(len(self.environment)))
            list_excl_z = [x for x in total_list if x not in z]
            remain = random.sample(list_excl_z,remaining_values)
            joinedlist = z + remain
            return joinedlist    

    def _capital_check(self, begin_portfolio, money_delta):
        portfolio_value_start = round(sum(begin_portfolio['Value_per_stock'])+money_delta,2)
        portfolio_value_now = round(sum(self.environment['Value_per_stock']),2)
        rest_value = round(portfolio_value_start - portfolio_value_now,2)
        if rest_value != 0:
            cond=self.environment['Value_per_stock'] > 10
            x = np.where(cond)
            x = np.array(x).tolist()[0]
            i = random.choice(x)
            self.environment.Value_per_stock.iloc[i] = self.environment.Value_per_stock.iloc[i] + rest_value
        else:
            print('Risk Check Complete!')

    def _weighted_allocation(self):
        weight_should = sum(self.environment['Value_per_stock']) / len(self.environment)
        self.environment['Weighted_allocation'] = self.environment['Value_per_stock'] / weight_should
        self.environment = self.environment[pd.to_numeric(self.environment['Risk'],errors='coerce').notnull()]

    def _analyst_ratings(self):
        self.environment = analyst_ratings(self.environment)

    def _get_trades(self, begin_portfolio):
        self.environment['trades'] = round(self.environment['Value_per_stock'] - begin_portfolio['Value_per_stock'],2)

    def run(self, begin_portfolio, money_delta):
        self._weighted_allocation()
        self._individual_deposit_withdraw_check(begin_portfolio, money_delta)
        self._capital_check(begin_portfolio, money_delta)
        self._get_trades(begin_portfolio)
        self._weighted_allocation()
        return self.environment