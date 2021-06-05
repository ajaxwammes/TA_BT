#how long should the code run for (in days)
secs_day = 86400
run_duration = secs_day*31

#length of original portfolio. This needs to be max 0.5*len(tickers), else money can be left uninvested
stocks_n = 25

#when an investment in a ticker is less  than this % of what it should be with the current capital, buy again
rebuy_percentage = 0.5

#the threshold for when a stock is considered low cap
low_cap_threshold = 50

#Change port to IB client you are using
#TWS paper trading:7497
#TWS money trading:7496
#IB Gateway paper trading: 4002
#IB Gateway money trading: 4001
port = 4002

""" STRATEGY """
#Financial products (CW, CE, EST, ToF, RE, PBF) - low risk
ticker_symbols = ['AWK', 'BMI', 'CWT', 'CWCO', 'ECL', 'ERII', 'AQUA', 'PNR', 'SBS', 'SJW', 'TTEK', 'XYL', 'ECOL',
           'CWST', 'CLH', 'DAR', 'HSC', 'RSG', 'VTNR', 'WCN', 'WM', 'HCCI', 'AQMS', 'CVA',
           'AMRC', 'AMAT', 'CGRN', 'WLDN', 'ITRI', 'ASPN', 'TT',
           'APTV', 'FUV', 'BEEM', 'NIU', 'BLDP', 'BLNK', 'NIO',
           'AMTX', 'BEP', 'NOVA', 'HASI', 'EBR', 'CSIQ', 'AQN',
           'BYND', 'TTCF', 'INGR'
            ]


#the duration between scans / ticker size (1,3,5,10,15,30)
ticker_size = 10

#ticker size, adapted form
ticker_size_mins = str(ticker_size) + ' ' + 'mins'

#the threshold value for the stochastic indicator
stoch_threshold = 99

#RSI base value (might differ caused by flex)
rsi_threshold = 80

#analyst rating threshold, after which to sell a stock (1 best - 5 worst)
analyst_rating_threshold = 2.8

""" TECHNICAL INDICATORS """

#ATR
#by how much should the ATR be multipied before a stock is sold / rebalanced should be 11
atr_multiplier = 11

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
