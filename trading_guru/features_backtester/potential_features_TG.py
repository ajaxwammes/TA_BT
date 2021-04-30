
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