from Backtest import Backtest
from DataScripts import stockData
from Screeners import MovingAverages
import pandas as pd
import datetime
import multiprocessing


# backtest data
# stockData = stockData.getStockData(fileName='adjClose')
# df = pd.read_csv('https://raw.githubusercontent.com/nvshah286/PyQuant/f312ae047cbf24567a6a03504867888fba40f4cc/DataFiles/adjClose.csv')
df = pd.read_csv('DataFiles/SP500AdjClose.csv')
df.set_index('Date', drop=True, inplace=True)
# df.to_csv('DataFiles/SP500AdjClose.csv')

summary = pd.DataFrame()
# generating the backtest object
impAverages = [(5, 10), (10, 20), (10, 50), (10, 70), (10, 100), (50, 200)]

hs = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80]
for i in hs:
    bkResult = Backtest.BackTest(func=MovingAverages.movingAverages,
                                 stockData=df,
                                 arguments=(10, 20),
                                 holdingPeriod=i)
    # calculating the backtest summary
    summary = pd.concat([summary, bkResult.summary()], axis=1)

names = [i for i in hs]
summary.columns = names
res = summary.transpose()
print(summary)
# summary.to_csv('DataFiles/Summary.csv')
