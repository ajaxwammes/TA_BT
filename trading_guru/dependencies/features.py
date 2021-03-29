import requests
import time
from . import strategy_hardcoded_values as SHV

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
        print(ticker, 'has no analyst rating')
    return rating


#new solution: 50 tickers in list, while ps calculation is /40. It will continue trying to buy stocks even when no money.
def what_tickers(app):
    app.reqAccountSummary(1, "All", "$LEDGER:USD")
    time.sleep(1)
    tickers = SHV.ticker_symbols
    return tickers
