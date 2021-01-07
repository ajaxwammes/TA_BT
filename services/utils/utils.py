import datetime
from futures3.thread import ThreadPoolExecutor
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import requests

from services.configs import risk_thresholds_levels as RTL

def analyst_ratings(environment):
    print('Checking analyst ratings of potential products...')
    companylist = list(environment['Ticker'])
    recommendations = []
    url_list = []
    lhs_url = RTL.lhs_url
    rhs_url = RTL.rhs_url
    for Value in companylist:
        url = lhs_url + Value + rhs_url
        url_list.append(url)
    with ThreadPoolExecutor(max_workers=10) as executer:
        try:
            for r in executer.map(requests.get, url_list):
                try:
                    result = r.json()['quoteSummary']['result'][0]
                    recommendations.append(result['financialData']['recommendationMean']['fmt'])
                except:
                    recommendations.append(0)
        except Exception:
            recommendations.append(0)
    environment['Analyst_rating'] = pd.to_numeric(recommendations)
    return environment

def risk(ticker):
    start = datetime.datetime.now() - datetime.timedelta(days=RTL.days_volatility)
    end = datetime.datetime.now()
    try:
        print("Calculating risk for",ticker)
        df = web.DataReader(ticker, RTL.market_data_provider, start, end)['Close']
        df = pd.Series.to_frame(df)
        df['ret'] = np.log(df.Close / df.Close.shift(1))
        vol = df['ret'].std() * np.sqrt(RTL.days_volatility/1.4484)
        return vol
    except KeyError:
        print('CHECK THIS PRODUCT, POSSIBLY NO LONGER EXISTS', ticker)