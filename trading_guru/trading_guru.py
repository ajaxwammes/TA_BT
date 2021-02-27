"""
TG_Bot
Created on Wed Sep 09 / Wed Oct 21 16:32:12
@author: mart.vos

#Strategy 12: Trading Guru

Technical indicators used:
    - ATR
    - RSI

Universe: Sustainable

Backtested performance Jan 2010 - Dec 2020
Return:     1010%
Return B-H: 780%
Sharpe:     3.12
Trades:     581
"""

# Import libraries
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import pandas as pd
import numpy as np
import threading
import time
from dependencies import strategy_hardcoded_values as SHV


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
        print(f'Time: {bar.date}, Open: {bar.open}, Close: {bar.close}')
        if reqId not in self.data:
            self.data[reqId] = [{"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume}]
        else:
            self.data[reqId].append({"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume})

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        print("NextValidId:", orderId)
        
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

    def accountSummary(self, reqId:int, account: str, tag: str, value: str, currency:str):
        super().accountSummary(reqId, account, tag, value, currency)
        x = value
        print(x[1])

        

def usTechStk(symbol,sec_type="STK",currency="USD",exchange="ISLAND"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    return contract 


def histData(req_num,contract,duration,candle_size):
    """extracts historical data"""
    app.reqHistoricalData(reqId=req_num,
                          contract=contract,
                          endDateTime='',
                          durationStr=duration,
                          barSizeSetting=candle_size,
                          whatToShow='ADJUSTED_LAST',
                          useRTH=1,
                          formatDate=1,
                          keepUpToDate=0,
                          chartOptions=[])	 # EClient function to request contract details


def websocket_con():
    app.run()


app = TradeApp()
app.connect(host='127.0.0.1', port=SHV.port, clientId=23)
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()


#Select how much money is allocated to each stock
capital_total = SHV.capital_total

#the capital per stock
capital = SHV.capital_total / SHV.stocks_n


def tickers_final(pos_n):
    if app.accountSummary() > capital and \
    pos_n == SHV.stocks_n:
        add_stocks = int(app.accountSummary()/capital)
        stocks_total = pos_n + add_stocks
        tickers = SHV.ticker_symbols[:stocks_total]
    else:
        tickers = SHV.ticker_symbols[:SHV.stocks_n]
    return tickers
    


#>>>>>>>>>>>>>>>> Storing trade app object in dataframe <<<<<<<<<<<<<<<<<<<

def dataDataframe(TradeApp_obj,symbols, symbol):
    "returns extracted historical data in dataframe format"
    df = pd.DataFrame(TradeApp_obj.data[symbols.index(symbol)])
    df.set_index("Date",inplace=True)
    return df


def MACD(DF,a=SHV.fast_moving_average,b=SHV.slow_moving_average,c=SHV.signal_line):
    df = DF.copy()
    df["MA_Fast"]=df["Close"].ewm(span=a,min_periods=a).mean()
    df["MA_Slow"]=df["Close"].ewm(span=b,min_periods=b).mean()
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=c,min_periods=c).mean()
    return df


def stochOscltr(DF,a=SHV.stoch_lookback_period,b=SHV.stoch_moving_average_window):
    """Stochastic Oscillator: over/undersold: >80 overbought and <20 oversold"""
    df = DF.copy()
    df['C-L'] = df['Close'] - df['Low'].rolling(a).min()
    df['H-L'] = df['High'].rolling(a).max() - df['Low'].rolling(a).min()
    df['%K'] = df['C-L']/df['H-L']*100
    #df['%D'] = df['%K'].ewm(span=b,min_periods=b).mean()
    return df['%K'].rolling(b).mean()


def atr(DF,n=SHV.atr_n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L']=abs(df['High']-df['Low'])
    df['H-PC']=abs(df['High']-df['Close'].shift(1))
    df['L-PC']=abs(df['Low']-df['Close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    #df['ATR'] = df['TR'].rolling(n).mean()
    df['ATR'] = df['TR'].ewm(com=n, min_periods=n).mean()*SHV.atr_multiplier
    return df['ATR']


def rsi(DF,n=SHV.rsi_n):
    df = DF.copy()
    df['delta']=df['Close'] - df['Close'].shift(1)
    df['gain']=np.where(df['delta']>=0,df['delta'],0)
    df['loss']=np.where(df['delta']<0,abs(df['delta']),0)
    avg_gain = []
    avg_loss = []
    gain = df['gain'].tolist()
    loss = df['loss'].tolist()
    for i in range(len(df)):
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(df['gain'].rolling(n).mean()[n])
            avg_loss.append(df['loss'].rolling(n).mean()[n])
        elif i > n:
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
    df['avg_gain']=np.array(avg_gain)
    df['avg_loss']=np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    return df['RSI']


#>>>>>>>>>>>>>>>>>>>> Define the orders you want to make <<<<<<<<<<<<<<<<<<<<

def marketOrder(direction,quantity):
    order = Order()
    order.action = direction
    order.orderType = "MKT"
    order.totalQuantity = quantity
    return order

def stopOrder(direction,quantity,st_price):
    order = Order()
    order.action = direction
    order.orderType = "STP"
    order.totalQuantity = quantity
    order.auxPrice = st_price
    return order

def limitOrder(direction,quantity,lmt_price):
    order = Order()
    order.action = direction
    order.orderType = "LMT"
    order.totalQuantity = quantity
    order.lmtPrice = lmt_price
    return order


#>>>>>>>>>>>>>>>>>>>>>>>>>>>> Actual Strategy <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def main():
    app.reqAccountSummary(9003, "All", "$LEDGER:USD")
    app.data = {}
    app.pos_df = pd.DataFrame(columns=['Account', 'Symbol', 'SecType',
                            'Currency', 'Position', 'Avg cost'])
    app.order_df = pd.DataFrame(columns=['PermId', 'ClientId', 'OrderId',
                                      'Account', 'Symbol', 'SecType',
                                      'Exchange', 'Action', 'OrderType',
                                      'TotalQty', 'CashQty', 'LmtPrice',
                                      'AuxPrice', 'Status'])
    app.reqPositions()
    time.sleep(2)
    pos_df = app.pos_df
    pos_df.drop_duplicates(inplace=True, ignore_index=True) #position callback tends to give duplicate values
    pos_n = len(pos_df)
    tickers = tickers_final(pos_n)
    app.reqOpenOrders()
    time.sleep(2)
    ord_df = app.order_df
    for ticker in tickers:
        print("starting pass-through for.....",ticker)
        histData(tickers.index(ticker),usTechStk(ticker),'1 M', SHV.ticker_size_mins)
        time.sleep(5)
        df = dataDataframe(app,tickers,ticker)
        df["stoch"] = stochOscltr(df)
        df["macd"] = MACD(df)["MACD"]
        df["signal"] = MACD(df)["Signal"]
        df["atr"] = atr(df)
#        df["adx"] = adx(df)
#        df["bollBnd_width"] = bollBnd(df)['BB_width']
#        df["bollBnd_up"] = bollBnd(df)['BB_up']
#        df["bollBnd_dn"] = bollBnd(df)['BB_dn']
        df.dropna(inplace=True)
        quantity = int(capital/df["Close"][-1])
        if quantity == 0:
            continue

        # You have no existing positions at all: simply make the trade
        if len(pos_df.columns)==0:
            try:
                if df["macd"][-1]> df["signal"][-1] and \
                    df["stoch"][-1]> SHV.stoch_threshold and \
                   df["stoch"][-1] > df["stoch"][-2]:
                       app.reqIds(-1)
                       time.sleep(2)
                       order_id = app.nextValidOrderId
                       if df.index[-1][-8:] != '21:45:00':
                        app.placeOrder(order_id,usTechStk(ticker),marketOrder("BUY",quantity))
                        app.placeOrder(order_id + 1, usTechStk(ticker),
                                       limitOrder("SELL", quantity*SHV.rebalance_perc, round(df["Close"][-1] + df["atr"][-1], 1)))
            except Exception as e:
                print(ticker, e)

        # You have existing DF with positions, but this ticker isn't in your pos DF: simply make the trade
        elif len(pos_df.columns)!=0 and ticker not in pos_df["Symbol"].tolist():
            try:
                if df["macd"][-1]> df["signal"][-1] and \
                    df["stoch"][-1]> SHV.stoch_threshold and \
                   df["stoch"][-1] > df["stoch"][-2]:
                       app.reqIds(-1)
                       time.sleep(2)
                       order_id = app.nextValidOrderId
                       if df.index[-1][-8:] != '21:45:00':
                        app.placeOrder(order_id,usTechStk(ticker),marketOrder("BUY",quantity))
                        app.placeOrder(order_id + 1, usTechStk(ticker),
                                       limitOrder("SELL", quantity*SHV.rebalance_perc, round(df["Close"][-1] + df["atr"][-1], 1)))
            except Exception as e:
                print(ticker, e)

        # You have existing DF with positions, and your ticker in in de pos DF, but the value is 0 (it's been bought but also already sold): simply make the trade
        elif len(pos_df.columns)!=0 and ticker in pos_df["Symbol"].tolist():
            if pos_df[pos_df["Symbol"]==ticker]["Position"].sort_values(ascending=True).values[-1] == 0:
                try:
                    if df["macd"][-1]> df["signal"][-1] and \
                        df["stoch"][-1]> SHV.stoch_threshold and \
                       df["stoch"][-1] > df["stoch"][-2]:
                       app.reqIds(-1)
                       time.sleep(2)
                       order_id = app.nextValidOrderId
                       if df.index[-1][-8:] != '21:45:00':
                           app.placeOrder(order_id + 1, usTechStk(ticker),
                                          limitOrder("SELL", quantity*SHV.rebalance_perc, round(df["Close"][-1] + df["atr"][-1], 1)))
                except Exception as e:
                    print(ticker, e)


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


#extract and store historical data in dataframe repetitively
starttime = time.time()

#when should the code stop running in sec -> 1 month
timeout = time.time() + SHV.run_duration

#How long should the code sleep in between runs (900 sleep time = 15min)
while time.time() <= timeout:
    main()
    print('Check done, going to sleep now')
    time.sleep(60*SHV.ticker_size - ((time.time() - starttime) % 60*SHV.ticker_size))