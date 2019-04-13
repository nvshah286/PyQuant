import pandas as pd
import datetime
from DataScripts import stockData
import matplotlib.pyplot as plt


# find the points where the 50 day crosses 200 dma from below.
# Identify those as Buy point
def movingAverages(series=None, shortTime=10, longTime=50):
    series = series['Adj Close']
    avgShort = series.rolling(shortTime).mean()
    avgLong = series.rolling(longTime).mean()
    buypts = (avgShort > avgLong) & (avgShort < avgLong.shift(1))
    return buypts


def movingAveragesExp(series=None, shortTime=10, longTime=50):
    series = series['Adj Close']
    avgShort = series.ewm(span=shortTime, adjust=False).mean()
    avgLong = series.ewm(span=longTime, adjust=False).mean()
    buypts = (avgShort > avgLong) & (avgShort < avgLong.shift(1))
    return buypts
