#how much money is a customer putting in the algorithm
capital_total = 50000

#seconds in a day
secs_day = 86400

#how long should the code run for (in seconds in sec-min-hour-days)
run_duration = secs_day*31

#length of original portfolio
stocks_n = 40

#Change port to IB client you are using
#TWS paper trading:7497
#TWS money trading:7496
#IB Gateway paper trading: 4002
#IB Gateway money trading: 4001
port = 7497

""" STRATEGY """
#companies selected -> comes from create portfolio script
ticker_symbols = ["WCN", "AQN", "RSG", "WM", "AWK", "OLED", "CWST", "SJW", "ETN", "CWT",
           "BMI", "BEP", "NEP", "TTEK", "CWCO", "CWEN", "APTV", "CLH", "POWI",
           "HASI", "ON", "SBS", "ERII", "ITRI", "AY", "TRN", "DAR", "AQUA", "CVA",
           "ORA", "AMRC", "WLDN", "HCCI", "TPIC", "CSIQ", "AZRE", "REGI",
           "OESX", "ASPN", "NOVA", "AMSC", "DQ", "PLUG", "VTNR", "AQMS", "BEEM"]


#the duration between scans / ticker size (1,3,5,10,15,30)
ticker_size = 15

#ticker size, adapted form
ticker_size_mins = str(ticker_size) + ' ' + 'mins'

#the threshold value for the stochastic indicator
stoch_threshold = 30

#percentage sell-off after rebalancing
rebalance_perc = 0.25


""" TECHNICAL INDICATORS """

#ATR
#by how much should the ATR be multipied before a stock is sold / rebalanced should be 11
atr_multiplier = 1

#what n is the ATR looking at
atr_n = 80

#moving averge values
fast_moving_average = 12
slow_moving_average = 26
signal_line = 9

#stochastic
stoch_lookback_period = 20
stoch_moving_average_window = 3

#RSI
rsi_n = 20
