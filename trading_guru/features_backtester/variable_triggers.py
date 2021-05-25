# range is 70 - 80
def RSI_variable(vol_df1, i):
    RSI_neutral = 75
    average_volatiliy = vol_df1['roll_mean'][i]
    current_volatility = vol_df1['mean'][i]
    if average_volatiliy > current_volatility:
        RSI = RSI_neutral - 1
    elif average_volatiliy < current_volatility:
        RSI = RSI_neutral + 1
    else:
        RSI = RSI_neutral
    return RSI
