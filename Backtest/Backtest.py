import pandas as pd
import datetime
from DataScripts import stockData
import matplotlib.pyplot as plt
from Screeners import MovingAverages


def backtest(func =None,stockData = None , buyPts = None, args = None):
    fun = MovingAverages.movingAverages
    stockData = MovingAverages.adjCloseData
    args = (10,50)
    buyPts1050 = stockData.apply(func=fun, axis=1, args=args)

