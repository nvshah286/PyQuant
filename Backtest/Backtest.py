import pandas as pd
import datetime
from DataScripts import stockData
from Screeners import MovingAverages
import numpy as np


def calcReturns(series=None, entryPoints=None, holdingPeriod=5):
    entryPoints.reset_index(drop=True, inplace=True)
    entryTime = entryPoints.index[entryPoints]
    retSeries = []
    for e in entryTime:
        ret = 100 * ((series[e + holdingPeriod] / series[e]) - 1)
        retSeries.append(ret)
    return round(np.nanmean(retSeries), ndigits=4)


# so buypts is a series of True/False where true indicates a buy point.
# need to calculate weekly return from each buy point.
def backtest(func=None, stockData=None, arguments=None, holdingPeriod=5):
    # func = MovingAverages.movingAverages
    # stockData = MovingAverages.adjCloseData
    # args = (5,10)

    # remove the last few rows from stockdata for getting the buypts as some buffer is needed to test forward looking returns
    testData = stockData.iloc[:-20, ]
    buyPts = testData.apply(func=func, args=arguments, axis=0)
    avgRetSeries = []
    for s in stockData.columns:
        print(s)
        avgRet = calcReturns(series=stockData[s], entryPoints=buyPts[s], holdingPeriod=holdingPeriod)
        avgRetSeries.append(avgRet)

    avgRetSeries = pd.Series(avgRetSeries)
    avgRetSeries.index = stockData.columns
    avgRetSeries.columns = ['AvgReturns']
    return (avgRetSeries)
