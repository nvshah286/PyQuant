from Backtest import Backtest
from DataScripts import stockData
from Screeners import MovingAverages
import pandas as pd

# backtest data
stockData = stockData.getStockData(fileName='adjClose')
stockData.set_index('Date', drop=True, inplace=True)

summary = pd.DataFrame()
# generating the backtest object
impAverages = [(5, 10), (10, 20)]

for i in impAverages:
    bkResult = Backtest.BackTest(func=MovingAverages.movingAverages,
                                 stockData=stockData,
                                 arguments=i,
                                 holdingPeriod=5)
    # calculating the backtest summary
    summary = pd.concat([summary, bkResult.summary()], axis=1)

names = [str(i) for i in impAverages]
summary = summary.transpose()
summary.index = names

print(summary)
summary.to_csv('DataFiles/Summary.csv')
