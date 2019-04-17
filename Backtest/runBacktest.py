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
                                fileName='SP500Data', update=False)

summary = pd.DataFrame()
# generating the backtest object

hp = [5, 10, 15, 20, 25, 30]

for h in hp:
    bk1 = Backtest.BackTest(func=Volatility.bollingerlow,
                            stockData=btData,
                            arguments=None,
                            holdingPeriod=5)
    s1 = bk1.summary()
    summary = summary.append(s1, ignore_index=True)

summary.index = hp
print(summary)

summary[['AvgNegativeReturn', 'AvgPositiveReturn', 'AvgReturn']].plot()
plt.title('Low Bollinger backtesting against SP500')

## Attempt to convert series into data frame

retDF = pd.DataFrame()
ser = bk1.btReturns

for s in ser.keys():
    temp = pd.DataFrame({'Symbol': s, 'ReturnSeries': ser[s]})
    retDF = retDF.append(temp, ignore_index=True)


## dropping Nan Values
retDF.dropna(inplace=True)

# attach the return series with the metadata csv file.
# (this means backtest needs to know which index we are testing against)

sp500metadata = pd.read_csv('DataFiles/SP500Companies.csv')[['Symbol', 'GICS Sector', 'GICS Sub Industry']]

allData = pd.merge(retDF, sp500metadata, on='Symbol')
allData.columns = ['RetSeries', 'Symbol', 'GICS_Sector', 'GICS_SubIndustry']

allData.to_csv('LowBollingerSP500Results.csv')
