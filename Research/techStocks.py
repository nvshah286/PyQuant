import datetime
import multiprocessing
import multiprocessing
import time
import timeit
from multiprocessing import Pool
from multiprocessing import cpu_count
import dask.dataframe as dd
import numpy as np
import pandas  as pd
import pandas as pd
import swifter
from dask.multiprocessing import get

from Backtest import Backtest
from DataScripts import stockData
from Screeners import MovingAverages

stockData = pd.read_csv(
    'https://raw.githubusercontent.com/nvshah286/PyQuant/f312ae047cbf24567a6a03504867888fba40f4cc/DataFiles/adjClose.csv')
stockData.set_index('Date', drop=True, inplace=True)

bkResult = Backtest.BackTest(func=MovingAverages.movingAverages,
                             stockData=stockData,
                             arguments=(10, 20),
                             holdingPeriod=5)

buyPts = bkResult.buyPoints()


def calcReturns(symbol=None, stockData=None, buyPoints=None):
    print(len(symbol))
    series = stockData[symbol]
    entryPoints = buyPoints[symbol]
    entryPoints.reset_index(drop=True, inplace=True)
    series.reset_index(drop=True, inplace=True)
    entryTime = entryPoints.index[entryPoints]
    exitVal = series[entryTime + 5]
    entryVal = series[entryTime]
    return list(100 * (exitVal.values / entryVal.values - 1))


def retSeries(symbols=None):
    testData = stockData
    buyPts = bkResult.buyPoints()
    aggSeries = symbols.apply(calcReturns, args=(testData, buyPoints))
    aggSeries.index = symbols
    return aggSeries
