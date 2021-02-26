#how much money is a customer putting in the algorithm
capital_total = 50000

#how long should the code run for (in seconds)
run_duration = 60*60*24*31

#the duration between scans / ticker size (1,3,5,10,15,30)
ticker_size = 15

#ticker size, adapted form
ticker_size_mins = str(ticker_size) + ' ' + 'mins'

#the threshold value for the stochastic indicator
stoch_threshold = 30

#by how much should the ATR be multipied before a stock is sold / rebalanced
atr_multiplier = 8