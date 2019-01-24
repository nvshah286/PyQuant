import ta
import pickle
import pandas as pd

# get the data

with open("DataFiles/SP500Data.pickle", 'rb') as f:
    stockData = pickle.load(f)


# playing around with cmf
def cmfupTrend(series=None, shortAvg=5):
    cmf = ta.chaikin_money_flow(high=series['High'],
                                low=series['Low'],
                                close=series['Close'],
                                volume=series['Volume'])

    buyPts = (cmf > 0) & (cmf > cmf.rolling(shortAvg).mean())
    return buyPts


buyPts = pd.Series()
for s in stockData:
    print(stockData.keys()[s])
    cmf = cmfupTrend(stockData[s], shortAvg=5)
    buyPts = pd.concat([buyPts, cmf], axis=1)

buyPts.drop(columns=[0], inplace=True)
buyPts.columns = stockData.keys()
