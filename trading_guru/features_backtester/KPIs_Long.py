# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 22:18:12 2020

@author: mart.vos

KPIs long hold
"""

import numpy as np


def CAGR(DF):
#function to calculate cumulative annual rate; DF should have return column    
    df = DF.copy()
    df['cum_return']= (1 + df['ret']).cumprod()
    n=1
    CAGR = (df['cum_return'].tolist()[-1])**(1/n)-1
    return CAGR


def volatility(DF):
    df = DF.copy()
#252 for 1 year, 1 day candles. *26 for 15min candles. e.g. 2 year,15min candles=252*2*26  
    vol = df['ret'].std() * np.sqrt(252*3*39)
    return vol


def sharpe(DF,rf_rate=0.025):
    df = DF.copy()
    sr = (CAGR(df)-rf_rate)/volatility(df)
    return sr


#target set 0, risk free rate 2.5%
def sortino(DF,target=0, rf_rate=0.025):
    df = DF.copy()
    df['cum_return'] = (1 + df['ret']).cumprod()
    df['downside_returns'] = 0
    df.loc[df['ret'] < target, 'downside_returns'] = df['cum_return']**2
    expected_return = df['cum_return'].mean()
    down_stdev = np.sqrt(df['downside_returns'].mean())
    sortino_ratio = (expected_return - rf_rate)/down_stdev
    return sortino_ratio


def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd
