from Backtest import Backtest
from Screeners import MovingAverages
import pandas as pd
from DataScripts import stockData
import datetime

symbols = ['TSLA', 'AAPL', 'NVDA', 'NFLX', 'AMZN', 'MU', 'GOOGL', 'FB']
startDate = datetime.datetime(2013, 1, 1)
endDate = datetime.datetime(2018, 11, 1)
stockData = stockData.getStockData(symbols=symbols,
                                   fileName='myfav',
                                   startDate=startDate,
                                   endDate=endDate)
stockData.set_index('Date', drop=True, inplace=True)

impAverages = [(10, 50), (10, 100), (50, 100), (50, 200)]

cmpResult = pd.Series()
for i in impAverages:
    result = Backtest.backtest(func=MovingAverages.movingAverages,
                               stockData=stockData,
                               arguments=i,
                               holdingPeriod=15)
    cmpResult = pd.concat([cmpResult, result], axis=1)
