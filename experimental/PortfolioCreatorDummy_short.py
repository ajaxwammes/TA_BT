# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 14:56:24 2020

@author: mart.vos

Input:
    1. Sustainable categories
    2. Customer ID
    3. Amount of money investing
    4. Risk level
    5. Static DF of environment
    
Output:
    1. Updated portfolio
    2. Customer ID
"""
from services.create_portfolio import PortfolioCreator
import pandas as pd

pd.options.mode.chained_assignment = None

all_products = pd.read_csv('dummy_input1.csv')

choices = [
            'Renewable energy',
           'Clean water and oceans',
           'Circular economy', 
           'Transportation of the future',
#           'Energy-saving technology'
#           'Plant-based food',
#           'Overall sustainability'
            ]

environment = all_products[all_products.Industry.isin(choices)]
 
customerID = 1001                                    
risk_level = 3
money_in_portfolio = 2000

environment = PortfolioCreator.portfolio_lmh(environment,money_in_portfolio,risk_level)
environment = PortfolioCreator.portfolio_check_dummy(environment,money_in_portfolio,risk_level,all_products)
environment = PortfolioCreator.value_per_stock(environment,money_in_portfolio)