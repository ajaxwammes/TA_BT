"""
TG_Bot
Created on Wed Sep 09, 16:32:12
@author: mart.vos

#Strategy 12: Trading Guru
Universe: Sustainable

Backtested performance Jan 2010 - Dec 2020
Return:     1010%
Return B-H: 780%
Sharpe:     3.12
Trades:     581
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import pandas as pd
import numpy as np
import threading
from futures3.thread import ThreadPoolExecutor
import time
from dependencies import strategy_hardcoded_values as SHV
from dependencies import technical_indicators
from dependencies import order_types
from dependencies import features


account_value = []


class TradeApp(EWrapper, EClient): 
    def __init__(self):
        EClient.__init__(self, self) 
        self.data = {}
        self.pos_df = pd.DataFrame(columns=['Account', 'Symbol', 'SecType',
                                            'Currency', 'Position', 'Avg cost'])
        self.order_df = pd.DataFrame(columns=['PermId', 'ClientId', 'OrderId',
                                              'Account', 'Symbol', 'SecType',
                                              'Exchange', 'Action', 'OrderType',
                                              'TotalQty', 'CashQty', 'LmtPrice',
                                              'AuxPrice', 'Status'])
        
    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data[reqId] = [{"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low,
                                 "Close": bar.close, "Volume": bar.volume}]
        else:
            self.data[reqId].append({"Date": bar.date, "Open":bar.open, "High": bar.high, "Low": bar.low,
                                     "Close": bar.close,  "Volume": bar.volume})

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        #print("NextValidId:", orderId)
        
    def position(self, account, contract, position, avgCost):
        super().position(account, contract, position, avgCost)
        dictionary = {"Account":account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Currency": contract.currency, "Position": position, "Avg cost": avgCost}
        self.pos_df = self.pos_df.append(dictionary, ignore_index=True)
        
    def positionEnd(self):
        print("Latest position data extracted")
        
    def openOrder(self, orderId, contract, order, orderState):
        super().openOrder(orderId, contract, order, orderState)
        dictionary = {"PermId":order.permId, "ClientId": order.clientId, "OrderId": orderId, 
                      "Account": order.account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Exchange": contract.exchange, "Action": order.action, "OrderType": order.orderType,
                      "TotalQty": order.totalQuantity, "CashQty": order.cashQty, 
                      "LmtPrice": order.lmtPrice, "AuxPrice": order.auxPrice, "Status": orderState.status}
        self.order_df = self.order_df.append(dictionary, ignore_index=True)

    def accountSummary(self, reqId: int, account: str, tag: str, value: str, currency: str):
        super().accountSummary(reqId, account, tag, value, currency)
        if tag == 'CashBalance':
            account_value.append(float(value))
            return value

def usTechStk(symbol, sec_type="STK", currency="USD", exchange="ISLAND"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    return contract 

#EClient function to request contract details
def histData(req_num, contract, duration, candle_size):
    """extracts historical data"""
    app.reqHistoricalData(reqId=req_num,
                          contract=contract,
                          endDateTime='',
                          durationStr=duration,
                          barSizeSetting=candle_size,
                          whatToShow='ADJUSTED_LAST',
                          useRTH=1,
                          formatDate=1,
                          keepUpToDate=False,
                          chartOptions=[])

def websocket_con():
    app.run()

app = TradeApp()
app.connect(host='127.0.0.1', port=SHV.port, clientId=23)
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()

#Storing trade app object in dataframe
def dataDataframe(TradeApp_obj, symbols, symbol):
    df = pd.DataFrame(TradeApp_obj.data[symbols.index(symbol)])
    df.set_index("Date", inplace=True)
    return df

def data_in_df(tickers, ticker):
    counter = 1
    while True:
        try:
            if counter > 3:
                print('Pass for now:', ticker)
                return 0
            df = dataDataframe(app, tickers, ticker)
        except Exception:
            print('Need extra time to fetch data...')
            time.sleep(5)
            counter = counter + 1
            continue
        return df

#the capital per stock
def capital(pos_df):
    capital_ps = None
    while capital_ps is None:
        try:
            money_invested = pos_df['Position']*pos_df['Avg cost']
            money_invested_sum = sum(money_invested)
            print('Money invested:', round(money_invested_sum, 2))
            total_money = account_value[-1] + money_invested_sum
            capital_ps = total_money / SHV.stocks_n
        except:
            pass
        return float(capital_ps)

def buy_conditions(ord_df, investment_per_stock, df, ticker, quantity, trade_count, max_trades):
    try:
        if df["macd"][-1] > df["signal"][-1] and \
        df["stoch"][-1] > SHV.stoch_threshold and \
        df["stoch"][-1] > df["stoch"][-2] and \
        features.analyst_ratings(ticker) < SHV.analyst_rating_threshold and \
        account_value[-1] > investment_per_stock and \
        len(ord_df[(ord_df["Symbol"] == ticker) & (ord_df["Action"] == 'BUY')]) == 0 and \
        trade_count <= max_trades:
            buy(ticker, trade_count, df, quantity)
    except Exception as e:
        print(ticker, e)

def buy(ticker, trade_count, df, quantity):
    print('buying', ticker)
    trade_count += 1
    app.reqIds(-1)
    time.sleep(2)
    order_id = app.nextValidOrderId
    app.placeOrder(order_id, usTechStk(ticker), order_types.marketOrder("BUY", quantity))
    time.sleep(2)
    quantity_adj = df["atr"][-1] / df["Close"][-1]
    app.placeOrder(order_id + 1, usTechStk(ticker),
                   order_types.limitOrder("SELL", np.clip(a=round(quantity * quantity_adj * SHV.rebalance_perc),
                                                          a_min=1, a_max=None),
                                          round(df["Close"][-1] + df["atr"][-1], 2)))

def sell_conditions(ord_df, df, pos_df, ticker, quantity):
    orders = (ord_df[ord_df["Symbol"] == ticker]["OrderId"])
    try:
        if features.analyst_ratings(ticker) > SHV.analyst_rating_threshold and \
        len(ord_df[(ord_df["Symbol"] == ticker) & (ord_df["Action"] == 'SELL')]) == 1:
            print('selling', ticker, 'triggered by analyst ratings')
            sell(ord_df, pos_df, ticker, orders)
        elif df["rsi"][-1] > SHV.rsi_threshold and df["b_band_width"][-1] < df["b_band_mean"][-1] and \
        len(ord_df[(ord_df["Symbol"] == ticker) & (ord_df["Action"] == 'SELL')]) == 1:
            print('selling', ticker, 'triggered by b_bands + RSI')
            sell(ord_df, pos_df, ticker, orders)
        else:
            limitorder_check(ord_df, ticker, df, quantity)
    except Exception as e:
        print(ticker, e)

def sell(ord_df, pos_df, ticker, orders):
    old_quantity = pos_df[pos_df["Symbol"] == ticker]["Position"].sort_values(ascending=True).values[-1]
    app.reqIds(-1)
    time.sleep(2)
    order_id = app.nextValidOrderId
    app.placeOrder(order_id, usTechStk(ticker), order_types.marketOrder("SELL", old_quantity))
    if len(orders) > 0:
        ord_id = ord_df[ord_df["Symbol"] == ticker]["OrderId"].sort_values(ascending=True).values[-1]
        app.cancelOrder(ord_id)

def limitorder_check(ord_df, ticker, df, quantity):
    orders = (ord_df[ord_df["Symbol"] == ticker]["OrderId"])
    if len(orders) == 0:
        print('warning:',ticker,'order has no LimitOrder: placing a new one')
        quantity_adj = df["atr"][-1] / df["Close"][-1]
        app.reqIds(-1)
        time.sleep(2)
        order_id = app.nextValidOrderId
        app.placeOrder(order_id + 1, usTechStk(ticker), order_types.limitOrder("SELL", np.clip(a=round(quantity * quantity_adj * SHV.rebalance_perc),
                                                                                a_min=1, a_max=None), round(df["Close"][-1] + df["atr"][-1], 2)))
    else:
        print('keep position for', ticker)


def main():
    print('Scan:', features.current_time())
    if features.afterHours() == False:
        app.data = {}
        app.pos_df = pd.DataFrame(columns=['Account', 'Symbol', 'SecType', 'Currency', 'Position', 'Avg cost'])
        app.order_df = pd.DataFrame(columns=['PermId', 'ClientId', 'OrderId', 'Account', 'Symbol', 'SecType',
                                             'Exchange', 'Action', 'OrderType', 'TotalQty', 'CashQty', 'LmtPrice',
                                             'AuxPrice', 'Status'])
        app.reqPositions()
        time.sleep(2)
        pos_df = app.pos_df
        pos_df.drop_duplicates(inplace=True, ignore_index=True)
        tickers = features.what_tickers(app)
        app.reqOpenOrders()
        time.sleep(2)
        ord_df = app.order_df
        ord_df.drop_duplicates(inplace=True, ignore_index=True)
        print('Account value:', round(account_value[-1], 2))
        investment_per_stock = capital(pos_df)
        max_trades = account_value[-1] / investment_per_stock
        trade_count = 0
        if account_value[-1] < investment_per_stock:
            print("All money is invested. TG will only look for sell orders")
        ord_df.drop_duplicates(inplace=True, ignore_index=True)
        with ThreadPoolExecutor(max_workers=len(SHV.ticker_symbols)) as executer:
            try:
                executer.map(ticker_scan(tickers, investment_per_stock, ord_df, trade_count, max_trades, pos_df))
            except Exception:
                pass
    else:
        print('Market is closed')


def ticker_scan(tickers, investment_per_stock, ord_df,trade_count, max_trades, pos_df):
    for ticker in tickers:
        print("scanning ticker.....", ticker)
        histData(tickers.index(ticker), usTechStk(ticker), '1 M', SHV.ticker_size_mins)
        time.sleep(2)
        df = data_in_df(tickers, ticker)
        if isinstance(df, pd.DataFrame):
            df["stoch"] = technical_indicators.stochOscltr(df)
            df["macd"] = technical_indicators.MACD(df)["MACD"]
            df["signal"] = technical_indicators.MACD(df)["Signal"]
            df["atr"] = technical_indicators.atr(df)
            df["rsi"] = technical_indicators.rsi(df)
            df["b_band_width"] = technical_indicators.bollBnd(df)["BB_width"]
            df["b_band_mean"] = technical_indicators.bollBnd(df)["BB_mean"]
            df.dropna(inplace=True)
            quantity = int(investment_per_stock / df["Close"][-1])
            if quantity == 0:
                continue

            # when you DON'T own the stock
            if ticker not in pos_df["Symbol"].tolist() or \
                    pos_df[pos_df["Symbol"] == ticker]["Position"].sort_values(ascending=True).values[-1] == 0:
                buy_conditions(ord_df, investment_per_stock, df, ticker, quantity, trade_count, max_trades)

            # when you DO own the stock
            elif pos_df[pos_df["Symbol"] == ticker]["Position"].sort_values(ascending=True).values[-1] > 0:
                sell_conditions(ord_df, df, pos_df, ticker, quantity)
        else:
            print(ticker, 'does not give a DF')
            pass


#Running the code + smart sleep
while True:
    minute_count = features.current_time_min()
    if int(minute_count) not in {0, 15, 30, 45}:
        time.sleep(3)
    else:
        main()
        print('>>>>>>>>>>>>> Check done, now going to sleep <<<<<<<<<<<<<<<<<<<')
        print('  ')
