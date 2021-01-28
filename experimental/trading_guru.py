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

#Change port to IB client you are using
#TWS paper trading:7497
#TWS money trading:7496
#IB Gateway paper trading: 4002
#IB Gateway money trading: 4001
app = TradeApp()
app.connect(host='127.0.0.1', port=7497, clientId=23)
con_thread = threading.Thread(target=websocket_con, daemon=True)
con_thread.start()

tickers = ["PBD", "SPWR", "BLDP", "AMSC", "TSLA", "HCCI", "VTNR", "CWST", "OLED", "SRCL", "BMI",
           "TTEK", "CWCO", "POWI", "BYND", "FSLR", "SEDG"]

#Select how much money is allocated to each stock
capital_total = 50000
capital = capital_total / len(tickers)

#>>>>>>>>>>>>>>>> Storing trade app object in dataframe <<<<<<<<<<<<<<<<<<<

def dataDataframe(TradeApp_obj,symbols, symbol):
    "returns extracted historical data in dataframe format"
    df = pd.DataFrame(TradeApp_obj.data[symbols.index(symbol)])
    df.set_index("Date",inplace=True)
    return df


def MACD(DF,a=12,b=26,c=9):
    """function to calculate MACD
       typical values a(fast moving average) = 12; 
                      b(slow moving average) =26;
                      c(signal line ma window) =9"""
    df = DF.copy()
    df["MA_Fast"]=df["Close"].ewm(span=a,min_periods=a).mean()
    df["MA_Slow"]=df["Close"].ewm(span=b,min_periods=b).mean()
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=c,min_periods=c).mean()
    return df


def stochOscltr(DF,a=20,b=3):
    """Stochastic Oscillator: over/undersold: >80 overbought and <20 oversold
       a = lookback period
       b = moving average window for %D"""
    df = DF.copy()
    df['C-L'] = df['Close'] - df['Low'].rolling(a).min()
    df['H-L'] = df['High'].rolling(a).max() - df['Low'].rolling(a).min()
    df['%K'] = df['C-L']/df['H-L']*100
    #df['%D'] = df['%K'].ewm(span=b,min_periods=b).mean()
    return df['%K'].rolling(b).mean()


def atr(DF,n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L']=abs(df['High']-df['Low'])
    df['H-PC']=abs(df['High']-df['Close'].shift(1))
    df['L-PC']=abs(df['Low']-df['Close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    #df['ATR'] = df['TR'].rolling(n).mean()
    df['ATR'] = df['TR'].ewm(com=n, min_periods=n).mean()*1.4
    return df['ATR']


def rsi(DF,n=20):
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

"""
Not using:

def limitOrder(direction,quantity,lmt_price):
    order = Order()
    order.action = direction
    order.orderType = "LMT"
    order.totalQuantity = quantity
    order.lmtPrice = lmt_price
    return order


def trailStopOrder (direction,quantity,tr_step,st_price):
    order = Order()
    order.action = direction
    order.orderType = "TRAIL"
    order.totalQuantity = quantity
    order.auxPrice = tr_step
    order.trailStopPrice = st_price
    return order
"""

#>>>>>>>>>>>>>>>>>>>>>>>>>>>> Actual Strategy <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Change this when adapting the strategy

def main():
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
    pos_df.drop_duplicates(inplace=True,ignore_index=True) # position callback tends to give duplicate values
    app.reqOpenOrders()
    time.sleep(2)
    ord_df = app.order_df
    for ticker in tickers:
        print("starting pass-through for.....",ticker)
        histData(tickers.index(ticker),usTechStk(ticker),'1 M', '15 mins')
        time.sleep(5)
        df = dataDataframe(app,tickers,ticker)
        df["stoch"] = stochOscltr(df)
        df["macd"] = MACD(df)["MACD"]
        df["signal"] = MACD(df)["Signal"]
        df["atr"] = atr(df, 60)
#        df["adx"] = adx(df)
#        df["bollBnd_width"] = bollBnd(df)['BB_width']
#        df["bollBnd_up"] = bollBnd(df)['BB_up']
#        df["bollBnd_dn"] = bollBnd(df)['BB_dn']
        df.dropna(inplace=True)
        quantity = int(capital/df["Close"][-1])
        if quantity == 0:
            continue

        # You have no existing positions at all: simply make the trade
        # df["macd"][-1]> df["signal"][-1] and \
        if len(pos_df.columns)==0:
            if df["stoch"][-1]> 30 and \
               df["stoch"][-1] > df["stoch"][-2]:
                   app.reqIds(-1)
                   time.sleep(2)
                   order_id = app.nextValidOrderId
                   app.placeOrder(order_id,usTechStk(ticker),marketOrder("BUY",quantity))
                   app.placeOrder(order_id+1,usTechStk(ticker),stopOrder("SELL",quantity,round(df["Close"][-1]-df["atr"][-1],1)))

        # You have existing DF with positions, but this ticker isn't in your pos DF: simply make the trade
        elif len(pos_df.columns)!=0 and ticker not in pos_df["Symbol"].tolist():
            if df["stoch"][-1]> 30 and \
               df["stoch"][-1] > df["stoch"][-2]:
                   app.reqIds(-1)
                   time.sleep(2)
                   order_id = app.nextValidOrderId
                   app.placeOrder(order_id,usTechStk(ticker),marketOrder("BUY",quantity))
                   app.placeOrder(order_id+1,usTechStk(ticker),stopOrder("SELL",quantity,round(df["Close"][-1]-df["atr"][-1],1)))

        # You have existing DF with positions, and your ticker in in de pos DF, but the value is 0 (it's been bought but also already sold): simply make the trade
        elif len(pos_df.columns)!=0 and ticker in pos_df["Symbol"].tolist():
            if pos_df[pos_df["Symbol"]==ticker]["Position"].sort_values(ascending=True).values[-1] == 0:
                if df["stoch"][-1]> 30 and \
                   df["stoch"][-1] > df["stoch"][-2]:
                   app.reqIds(-1)
                   time.sleep(2)
                   order_id = app.nextValidOrderId
                   app.placeOrder(order_id,usTechStk(ticker),marketOrder("BUY",quantity))
                   app.placeOrder(order_id+1,usTechStk(ticker),stopOrder("SELL",quantity,round(df["Close"][-1]-df["atr"][-1],1)))

            # You have existing DF with positions, and your ticker is in de pos DF, and the value is > 0: Cancel the old stop order and place a new stop order
            elif pos_df[pos_df["Symbol"]==ticker]["Position"].sort_values(ascending=True).values[-1] > 0:
                try:
                    ord_id = ord_df[ord_df["Symbol"]==ticker]["OrderId"].sort_values(ascending=True).values[-1]
                except IndexError:
                    pass
                else:
                    ord_id = ord_df[ord_df["Symbol"] == ticker]["OrderId"].sort_values(ascending=True).values[0]
                old_quantity = pos_df[pos_df["Symbol"]==ticker]["Position"].sort_values(ascending=True).values[-1]
                app.cancelOrder(ord_id)
                app.reqIds(-1)
                time.sleep(2)
                order_id = app.nextValidOrderId
                app.placeOrder(order_id,usTechStk(ticker),stopOrder("SELL",old_quantity,round(df["Close"][-1]-df["atr"][-1],1)))


#extract and store historical data in dataframe repetitively
starttime = time.time()

#when should the code stop running in sec -> 1 month
timeout = time.time() + 60*60*696

#How long should the code sleep in between runs (900 sleep time = 15min)
while time.time() <= timeout:
    main()
    print('Check done, going to sleep now')
    time.sleep(900 - ((time.time() - starttime) % 900.0))