"""
#Not being used right now:

#BollingerBands
def bollBnd(DF, n=20):
    df = DF.copy()
#    df["MA"] = df['Close'].rolling(n).mean() #simple moving average
    df["MA"] = df['Close'].ewm(span=n,min_periods=n).mean() #exponential movinga avg
    df["BB_up"] = df['MA'] + 2*df['Close'].rolling(n).std(ddof=0)
    df["BB_dn"] = df['MA'] - 2*df['Close'].rolling(n).std(ddof=0)
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    return df


#ADX: to see how a stock is trending
def adx(DF,n=20):
    df2 = DF.copy()
    df2['H-L']=abs(df2['High']-df2['Low'])
    df2['H-PC']=abs(df2['High']-df2['Close'].shift(1))
    df2['L-PC']=abs(df2['Low']-df2['Close'].shift(1))
    df2['TR']=df2[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df2['+DM']=np.where((df2['High']-df2['High'].shift(1))>(df2['Low'].shift(1)-df2['Low']),df2['High']-df2['High'].shift(1),0)
    df2['+DM']=np.where(df2['+DM']<0,0,df2['+DM'])
    df2['-DM']=np.where((df2['Low'].shift(1)-df2['Low'])>(df2['High']-df2['High'].shift(1)),df2['Low'].shift(1)-df2['Low'],0)
    df2['-DM']=np.where(df2['-DM']<0,0,df2['-DM'])

    df2["+DMMA"]=df2['+DM'].ewm(span=n,min_periods=n).mean()
    df2["-DMMA"]=df2['-DM'].ewm(span=n,min_periods=n).mean()
    df2["TRMA"]=df2['TR'].ewm(span=n,min_periods=n).mean()

    df2["+DI"]=100*(df2["+DMMA"]/df2["TRMA"])
    df2["-DI"]=100*(df2["-DMMA"]/df2["TRMA"])
    df2["DX"]=100*(abs(df2["+DI"]-df2["-DI"])/(df2["+DI"]+df2["-DI"]))

    df2["ADX"]=df2["DX"].ewm(span=n,min_periods=n).mean()

    return df2['ADX']
"""

"""
def trailStopOrder (direction,quantity,tr_step,st_price):
    order = Order()
    order.action = direction
    order.orderType = "TRAIL"
    order.totalQuantity = quantity
    order.auxPrice = tr_step
    order.trailStopPrice = st_price
    return order
    
def stopOrder(direction,quantity,st_price):
    order = Order()
    order.action = direction
    order.orderType = "STP"
    order.totalQuantity = quantity
    order.auxPrice = st_price
    return order
"""

'''
#refresh stoploss order
            # You have existing DF with positions, and your ticker is in de pos DF, and the value is > 0: Cancel the old stop order and place a new stop order
            elif pos_df[pos_df["Symbol"]==ticker]["Position"].sort_values(ascending=True).values[-1] > 0:
                try:
                    ord_id = ord_df[ord_df["Symbol"]==ticker]["OrderId"].sort_values(ascending=True).values[-1]
                    app.cancelOrder(ord_id)
                    old_quantity = pos_df[pos_df["Symbol"]==ticker]["Position"].sort_values(ascending=True).values[-1]
                    app.reqIds(-1)
                    time.sleep(2)
                    if df.index[-1][-8:] != '21:45:00':
                        order_id = app.nextValidOrderId
                        app.placeOrder(order_id, usTechStk(ticker),
                                       stopOrder("SELL", old_quantity, round(df["Close"][-1]+df["atr"][-1], 1)))
                except Exception as e:
                    print(ticker, e)
'''

'''
def tickers_final(pos_n):
    app.reqAccountSummary(1, "All", "$LEDGER:USD")
    time.sleep(1)
    x = int(float(account_value[-1]))
    if SHV.stocks_n > pos_n:
        n_open = SHV.stocks_n - pos_n
        print('number of stocks with value zero:',n_open)
        if (x - (n_open*capital_ps)) / capital_ps >= 1:
            add_stocks = int((x - (n_open*capital_ps)) / capital_ps)
            stocks_total = SHV.stocks_n + add_stocks
            tickers = SHV.ticker_symbols[:stocks_total]
            print(add_stocks, " NEW STOCKS TO INVEST, NEW TOTAL:,", stocks_total)
            print('added stocks from: ', SHV.ticker_symbols[SHV.stocks_n])
        else:
            tickers = SHV.ticker_symbols[:SHV.stocks_n]
            print('value not enough to add new stocks to universe')
    else:
        if (x / capital_ps) > 1:
            add_stocks = int(x / capital_ps)
            stocks_total = int(pos_n + add_stocks)
            tickers = SHV.ticker_symbols[:stocks_total]
            print(add_stocks, "new stocks to invest, total:", stocks_total)
            print('added stocks from: ', SHV.ticker_symbols[pos_n])
        else:
            tickers = SHV.ticker_symbols[:pos_n]
            print('total stocks:', pos_n, 'not enough capital to add new stocks')
    return tickers
'''