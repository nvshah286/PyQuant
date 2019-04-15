from Backtest import Backtest
from Screeners import MovingAverages
import pandas as pd
from DataScripts import stockData

# fetch the tickers
tickers = stockData.getTickers('SP500')

# get data for those tickers
btData = stockData.getIndexData(fileName='SP500Data', update=False)

summary = pd.DataFrame()
# generating the backtest object

bk1 = Backtest.BackTest(func=MovingAverages.movingAverages,
                        stockData=btData,
                        arguments=(10,20),
                        holdingPeriod=5)
s1 = bk1.summary()

s1