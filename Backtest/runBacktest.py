from Backtest import Backtest
from Screeners import MovingAverages
import pandas as pd
from DataScripts import stockData

# fetch the tickers
tickers = stockData.getTickers('R3000')

# get data for those tickers
r3000Data = stockData.getIndexData(fileName='R3000Data', update=False)

summary = pd.DataFrame()
# generating the backtest object

bk1 = Backtest.BackTest(func=MovingAverages.movingAverages,
                        stockData=r3000Data,
                        arguments=(10, 20),
                        holdingPeriod=5)
s1 = bk1.summary()

# impAverages = [(5, 10), (10, 20), (10, 50), (10, 70), (10, 100), (50, 200)]
#
# hs = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80]
# for i in hs[:3]:
#     bkResult = Backtest.BackTest(func=MovingAverages.movingAverages,
#                                  stockData=r3000Data,
#                                  arguments=(10, 20),
#                                  holdingPeriod=i)
#     # calculating the backtest summary
#     summary = pd.concat([summary, bkResult.summary()], axis=1)
#
# names = [i for i in hs]
# summary.columns = names
# res = summary.transpose()
# print(summary)
# # summary.to_csv('DataFiles/Summary.csv')
