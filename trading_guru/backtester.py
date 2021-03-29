# -*- coding: utf-8 -*-
"""
Created on Sat Oct 3 15:34:57 2020

Yes overnight
Close - Close

Market: Sustainable - Trading Guru
Products: Nasdaq + NYSE

@author: mart.vos
"""

# Import libraries
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import pandas as pd
import threading
#import matplotlib
import time
import numpy as np
from copy import deepcopy
from trading_guru.dependencies import technical_indicators as TI
from trading_guru.features_backtester import KPIs_Long as KL, KPIs_IntraDay as KI


class TradeApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}
        
    def historicalData(self, reqId, bar):
        if reqId not in self.data:
            self.data[reqId] = [{"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume}]
        else:
            self.data[reqId].append({"Date":bar.date,"Open":bar.open,"High":bar.high,"Low":bar.low,"Close":bar.close,"Volume":bar.volume})
        #print("reqID:{}, date:{}, open:{}, high:{}, low:{}, close:{}, volume:{}".format(reqId,bar.date,bar.open,bar.high,bar.low,bar.close,bar.volume))

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
                          keepUpToDate=False,
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
time.sleep(1) # some latency added to ensure that the connection is established

#Financial products
tickers = ["AAPL", "NTGR", "INTC", "FB", "ORC", "NVDA"]

#Capital per stock USD
Capital = 5800

#Costs per trade USD
Costs_per_trade = 0.05

def dataDataframe(TradeApp_obj,symbols, symbol):
    df = pd.DataFrame(TradeApp_obj.data[symbols.index(symbol)])
    df.set_index("Date", inplace=True)
    return df

def data_in_df(tickers, ticker):
    while True:
        try:
            df = dataDataframe(app, tickers, ticker)
        except Exception:
            print('Need extra time to fetch data...')
            time.sleep(10)
            continue
        return df

def get_data():
    data = {}
    for ticker in tickers:
        print("Fetching data for", ticker)
        histData(tickers.index(ticker), usTechStk(ticker), '5 Y', '1 hour')
        time.sleep(10)
        data[ticker] = data_in_df(tickers, ticker)
    return data


historicalData = get_data()


#len(app.data)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Backtesting <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#merging the indicators in 1 DF 
ohlc_dict = deepcopy(historicalData)
tickers_signal = {}
tickers_ret = {}
trade_count = {}
trade_data = {}
for ticker in tickers:
    print("Calculating for ",ticker)
    ohlc_dict[ticker]["stoch"] = TI.stochOscltr(ohlc_dict[ticker])
    ohlc_dict[ticker]["macd"] = TI.MACD(ohlc_dict[ticker])["MACD"]
    ohlc_dict[ticker]["signal"] = TI.MACD(ohlc_dict[ticker])["Signal"]
    ohlc_dict[ticker]['time'] = ohlc_dict[ticker].index.str[10:]
#    ohlc_dict[ticker]['day_sav'] = TI.daylight_savings(ohlc_dict[ticker])
    ohlc_dict[ticker]["atr"] = TI.atr(ohlc_dict[ticker],80)
    ohlc_dict[ticker]["rsi"] = TI.rsi(ohlc_dict[ticker],20)
    ohlc_dict[ticker]["slippage"] = TI.slippage(ohlc_dict[ticker])
    ohlc_dict[ticker]["trading_costs"] = TI.trading_costs(ohlc_dict[ticker],Capital)
#    ohlc_dict[ticker]["adx"] = TI.adx(ohlc_dict[ticker])
    ohlc_dict[ticker]["bollBnd_width"] = TI.bollBnd(ohlc_dict[ticker])['BB_width']
    ohlc_dict[ticker]["bollBnd_up"] = TI.bollBnd(ohlc_dict[ticker])['BB_up']
    ohlc_dict[ticker]["bollBnd_dn"] = TI.bollBnd(ohlc_dict[ticker])['BB_dn']
    ohlc_dict[ticker]["bollBnd_mean"] = TI.bollBnd(ohlc_dict[ticker])['BB_mean']
    ohlc_dict[ticker].dropna(inplace=True)
    trade_count[ticker] = 0
    tickers_signal[ticker] = ""
    tickers_ret[ticker] = [0]
    trade_data[ticker] = {}
        


#calculating return of strategy
for ticker in tickers:
    print("Calculating daily returns for ",ticker)
    for i in range(1,len(ohlc_dict[ticker])):
        if tickers_signal[ticker] == "":
            tickers_ret[ticker].append(0)
            if ohlc_dict[ticker]["macd"][i]> ohlc_dict[ticker]["signal"][i] and \
                ohlc_dict[ticker]["stoch"][i]> 30 and \
               ohlc_dict[ticker]["stoch"][i] > ohlc_dict[ticker]["stoch"][i-1]:
                   tickers_signal[ticker] = "Buy"
                   trade_count[ticker] += 1
                   trade_data[ticker][trade_count[ticker]] = [ohlc_dict[ticker]["Close"][i]]
                
        elif tickers_signal[ticker] == "Buy":
            if ohlc_dict[ticker]["Open"][i] >= ohlc_dict[ticker]["Close"][i-1] + ohlc_dict[ticker]["atr"][i-1]:
                tickers_signal[ticker] = ""
                trade_data[ticker][trade_count[ticker]].append((ohlc_dict[ticker]["Open"][i] - ohlc_dict[ticker]["slippage"][i]))
                trade_count[ticker]+=1
                tickers_ret[ticker].append((ohlc_dict[ticker]["Open"][i]
                                             -ohlc_dict[ticker]["slippage"][i])
                                            /(ohlc_dict[ticker]["Close"][i-1])-1)


            elif ohlc_dict[ticker]["High"][i] >= ohlc_dict[ticker]["Close"][i-1] + ohlc_dict[ticker]["atr"][i-1]:
                tickers_signal[ticker] = ""
                trade_data[ticker][trade_count[ticker]].append((ohlc_dict[ticker]["Close"][i-1] + ohlc_dict[ticker]["atr"][i-1] - ohlc_dict[ticker]["slippage"][i]))
                trade_count[ticker]+=1
                tickers_ret[ticker].append((ohlc_dict[ticker]["Close"][i-1]
                                             +ohlc_dict[ticker]["atr"][i-1]
                                             -ohlc_dict[ticker]["slippage"][i-1])
                                           /(ohlc_dict[ticker]["Close"][i-1])-1)

                                               
            else:
                tickers_ret[ticker].append((ohlc_dict[ticker]["Close"][i]/ohlc_dict[ticker]["Close"][i-1])-1)
                
    if trade_count[ticker]%2 != 0:
        trade_data[ticker][trade_count[ticker]].append(ohlc_dict[ticker]["Close"][i])
                    
    ohlc_dict[ticker]["ret"] = np.array(tickers_ret[ticker])


# make data frame to show returns of all tickers per time period
strategy_df = pd.DataFrame()
for ticker in tickers:
    strategy_df[ticker] = ohlc_dict[ticker]["ret"]
  
#assuming that there is equal amount of capital allocated/invested to each stock    
strategy_df["ret"] = strategy_df.mean(axis=1)

#>>>>>>>>>>>>>>>>>>>> Get Intra-day KPIs of strategy <<<<<<<<<<<<<<<<<<<<<<<

# calculating overall strategy's KPIs
trade_df = {}
for ticker in tickers:
    trade_df[ticker] = pd.DataFrame(trade_data[ticker]).T
    trade_df[ticker].columns = ["trade_entry_pr", "trade_exit_pr"]
    trade_df[ticker]["return"] = (trade_df[ticker]["trade_exit_pr"]/trade_df[ticker]["trade_entry_pr"])

win_rate = {}
mean_ret_pt = {}
mean_ret_pwt = {}
mean_ret_plt = {}
max_cons_loss = {}
for ticker in tickers:
    print("calculating intraday KPIs for ", ticker)
    win_rate[ticker] = KI.winRate(trade_df[ticker])
    mean_ret_pt[ticker] = KI.meanretpertrade(trade_df[ticker])
    mean_ret_pwt[ticker] = KI.meanretwintrade(trade_df[ticker])
    mean_ret_plt[ticker] = KI.meanretlostrade(trade_df[ticker])

KPI_ID_df = pd.DataFrame([win_rate,mean_ret_pt,mean_ret_pwt,mean_ret_plt],
                      index=["Win Rate","MR Per Trade","MR Per WT", "MR Per LT"])
print(KPI_ID_df.T)

#Intra-day KPIs - Overall
wrs = sum(KPI_ID_df.T['Win Rate'])/len(KPI_ID_df.T['Win Rate'])
mrpt = sum(KPI_ID_df.T['MR Per Trade'])/len(KPI_ID_df.T['MR Per Trade'])
mrpwt = sum(KPI_ID_df.T['MR Per WT'])/len(KPI_ID_df.T['MR Per WT'])
mrplt = sum(KPI_ID_df.T['MR Per LT'])/len(KPI_ID_df.T['MR Per LT'])

IntraDay_Indicators = pd.DataFrame([wrs, mrpt, mrpwt, mrplt],
                      index=["Win Rate","MR Per Trade","MR Per WT", "MR Per LT"])      
print(IntraDay_Indicators.T)


#>>>>>>>>>>>>>>>>>>>> Get General KPIs of strategy <<<<<<<<<<<<<<<<<<<<<<<

#General KPIs - per product
cagr = {}
sharpe = {}
sortinos = {}
max_drawdown = {}
total_trades_ind = {}
for ticker in tickers:
    print("calculating KPIs for ",ticker)      
    cagr[ticker] =  KL.CAGR(ohlc_dict[ticker])
    sharpe[ticker] =  KL.sharpe(ohlc_dict[ticker])
    sortinos[ticker] =  KL.sortino(ohlc_dict[ticker])
    max_drawdown[ticker] =  KL.max_dd(ohlc_dict[ticker])
    total_trades_ind[ticker] = trade_count[ticker]  
    
KPI_df = pd.DataFrame([cagr,sharpe,sortinos,max_drawdown,total_trades_ind],index=["Return","Sharpe","Sortino","Max Drawdown","Total Trades"])
print(KPI_df.T)

#General KPIs - (now 2,5% risk free rate, target = 0%)
CAGR_strat = KL.CAGR(strategy_df)
Sortino_strat = KL.sortino(strategy_df)
Sharpe_strat = KL.sharpe(strategy_df)
Max_Drawdown_strat = KL.max_dd(strategy_df)
Total_trades = sum(trade_count.values())

#Get returns trading costs included
Total_win = (wrs/100)*Total_trades*mrpwt*Capital
Total_loss = ((100-wrs)/100)*Total_trades*mrplt*Capital
Return_Strat = Total_win - abs(Total_loss)
begin_cap = len(tickers)*Capital
Return_perc = (begin_cap+Return_Strat)/begin_cap-1

General_indicators = pd.DataFrame([CAGR_strat,Sortino_strat,Sharpe_strat,Max_Drawdown_strat,Total_trades],index=['Ret alt.','Sortino','Sharpe','Max Drawdown','Total Trades'])
print(General_indicators.T)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Visuals <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
 
# vizualization of strategy return
(1+strategy_df["ret"]).cumprod().plot()


# vizualization of strategy per stock
(1+ohlc_dict[ticker]["ret"]).cumprod().plot()

#Plot return per trade (only for 1 stock, stock can be changed be changing 1st ticker)
((trade_df['WM']["return"]-1)*100).plot()

# creating dataframe with daily returns
strategy_df.index = pd.to_datetime(strategy_df.index)
strategy_df.index = strategy_df.index.tz_localize('Europe/Berlin').tz_convert('America/Indiana/Petersburg')    
daily_ret_df = strategy_df.resample("D").sum(min_count=1).dropna()
hhh = daily_ret_df['ret']
n = 250
ax = hhh.plot(kind='bar')
ticks = ax.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in ax.xaxis.get_ticklabels()]
ax.xaxis.set_ticks(ticks[::n])
ax.xaxis.set_ticklabels(ticklabels[::n])
ax.figure.show()

#>>>>>>>>>>>>>>>>>>>>>>>>>> Buy-Hold Strategy <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#For buy-hold strategy
bh_data = deepcopy(historicalData)

for ticker in tickers:
    bh_data[ticker]["ReturnsBH"] = TI.ReturnsBH(bh_data[ticker])
    
strategy_df2 = pd.DataFrame()
for ticker in tickers:
    strategy_df2[ticker] = bh_data[ticker]["ReturnsBH"]
    
strategy_df2["ret"] = strategy_df2.mean(axis=1)

CAGR_BH = KL.CAGR(strategy_df2)
Max_dd_BH = KL.max_dd(strategy_df2)

BH_df = pd.DataFrame([CAGR_BH,Max_dd_BH],index=["CAGR","Max dd"])
print(BH_df.T)

#Plot B-H strategy

(1+strategy_df2["ret"]).cumprod().plot()
    