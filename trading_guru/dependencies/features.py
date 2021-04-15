import requests
import time as t
from . import strategy_hardcoded_values as SHV
import pytz
from pytz import timezone
from datetime import datetime as dd
from datetime import time



def analyst_ratings(ticker):
    try:
        lhs_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
        rhs_url = '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&' \
              'modules=upgradeDowngradeHistory,recommendationTrend,' \
              'financialData,earningsHistory,earningsTrend,industryTrend&' \
              'corsDomain=finance.yahoo.com'
        url = lhs_url + ticker + rhs_url
        r = requests.get(url)
        result = r.json()['quoteSummary']['result'][0]
        rating_float = result['financialData']['recommendationMean']['fmt']
        rating = float(rating_float)
    except Exception:
        rating = 0
        print('warning:', ticker, 'has no analyst rating')
    return rating

#new solution: 50 tickers in list, while ps calculation is /40. It will continue trying to buy stocks even when no money.
def what_tickers(app):
    app.reqAccountSummary(1, "All", "$LEDGER:USD")
    t.sleep(1)
    tickers = SHV.ticker_symbols
    return tickers

def current_time():
    tz = timezone('US/Eastern')
    now = dd.now(tz)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def current_time_min():
    tz = timezone('US/Eastern')
    now = dd.now(tz)
    dt_string = now.strftime("%M")
    return dt_string


def afterHours():
    tz = pytz.timezone('US/Eastern')
    now = dd.now(tz)
    now_time = now.time()
    market_open = time(9, 30)
    market_close = time(16, 0)
    if market_open <= now_time <= market_close and \
    dd.today().weekday() < 5:
        return False
    else:
        return True
