import requests
import time
from . import strategy_hardcoded_values as SHV
import datetime, pytz, holidays

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
    time.sleep(1)
    tickers = SHV.ticker_symbols
    return tickers


'''def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def afterHours(now = None):
    tz = pytz.timezone('US/Eastern')
    us_holidays = holidays.US()
    now = datetime.datetime.now(tz)
    if not now:
        openTime = datetime.time(hour = 9, minute = 30, second = 0)
        closeTime = datetime.time(hour = 16, minute = 0, second = 0)
    # If a holiday
    if now.strftime('%Y-%m-%d') in us_holidays:
        print('true')
    # If before 0930 or after 1600
    if (now.time() < openTime) or (now.time() > closeTime):
        return True
    # If it's a weekend
    if now.date().weekday() > 4:
        return True
    else:
        return False'''