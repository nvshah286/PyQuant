import pandas as pd
import datetime
from DataScripts import stockData
import matplotlib.pyplot as plt


# startDate = datetime.datetime(2010,1,1)
# endDate = datetime.datetime(2018,11,8)
#
# adjCloseData = stockData.getStockData(fileName='adjClose',
#                                       value ='Adj Close',
#                                       startDate= startDate,
#                                       endDate = endDate)


# find the points where the 50 day crosses 200 dma from below.
# Identify those as Buy point
def movingAverages(series=None, shortTime = 10, longTime = 50):
    avgShort = series.rolling(shortTime).mean()
    avgLong = series.rolling(longTime).mean()
    buypts = (avgShort > avgLong) & (avgShort < avgLong.shift(1))
    return buypts
