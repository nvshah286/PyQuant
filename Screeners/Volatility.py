import ta


def bollingerlow(series=None, n=14):
    series = series['Adj Close']
    buyPts = ta.bollinger_hband_indicator(series, n=n)
    buyPts.loc[buyPts == 1] = True
    buyPts.loc[buyPts != 1] = False
    return buyPts
