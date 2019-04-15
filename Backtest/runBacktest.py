from Backtest import Backtest
from Screeners import MovingAverages
import pandas as pd
from DataScripts import stockData
from Screeners import Volatility
import matplotlib.pyplot as plt

# fetch the tickers
tickers = stockData.getTickers('SP500')

# get data for those tickers
btData = stockData.getIndexData(symbols=tickers,
                                fileName='SP500Data', update=True)

summary = pd.DataFrame()
# generating the backtest object

hp = [5, 10, 15, 20, 25, 30]

for h in hp:
    bk1 = Backtest.BackTest(func=Volatility.bollingerlow,
                            stockData=btData,
                            arguments=None,
                            holdingPeriod=h)
    s1 = bk1.summary()
    summary = summary.append(s1, ignore_index=True)

summary.index = hp
print(summary)

summary[['AvgNegativeReturn', 'AvgPositiveReturn', 'AvgReturn']].plot()
plt.title('Low Bollinger backtesting against SP500')
