import numpy as np
import pandas as pd


# creating backtest class.
class BackTest:

    def __init__(self, func=None, stockData=None, arguments=None, holdingPeriod=5):
        self.func = func
        self.args = arguments
        self.holdingPeriod = holdingPeriod
        self.testData = stockData.iloc[: (holdingPeriod * -4), ]
        self.allData = stockData

    def buyPoints(self):
        buyPts = self.testData.apply(func=self.func, args=self.args, axis=0)
        return buyPts

    def tradeCounts(self):
        buyPts = self.buyPoints()
        tradeCounts = buyPts.apply(sum, axis=0)
        return tradeCounts

    def calcReturns(self, s=None, stockData=None, buyPoints=None):
        print(s)
        series = stockData[s]
        series.reset_index(drop=True, inplace=True)
        entryPoints = buyPoints[s]
        entryPoints.reset_index(drop=True, inplace=True)
        entryTime = entryPoints.index[entryPoints]
        exitVal = series[entryTime + self.holdingPeriod]
        entryVal = series[entryTime]
        return list(100 * (exitVal.values / entryVal.values - 1))

    def retSeries(self):
        symbols = pd.Series(self.allData.columns)
        buyPoints = self.buyPoints()
        aggSeries = symbols.apply(self.calcReturns, args=(self.allData, buyPoints))
        aggSeries.index = symbols
        return aggSeries

    def summary(self):
        allSeries = []
        for s in self.retSeries():
            allSeries += s;
        allSeries = pd.Series(allSeries)
        posNeg = allSeries >= 0
        df = pd.DataFrame({'Returns': allSeries, 'PosNeg': posNeg})
        summaryDF = df.groupby('PosNeg')['Returns'].agg(['mean', 'std', 'count'])
        winRatio = round(100 * (summaryDF.loc[True, 'count'] / len(df)), ndigits=4)
        avgPosReturn = round(summaryDF.loc[True, 'mean'], ndigits=4)
        avgNegReturn = round(summaryDF.loc[False, 'mean'], ndigits=4)
        avgRetOverall = round(np.nanmean(df.Returns), ndigits=4)
        avgTrades = round(sum(self.tradeCounts()) / len(self.testData.columns), ndigits=3)

        summary = {'AvgReturn': avgRetOverall,
                   'AvgPositiveReturn': avgPosReturn,
                   'AvgNegativeReturn': avgNegReturn,
                   'WinRatio': winRatio,
                   'AvgTrades': avgTrades
                   }
        return pd.Series(summary)

# write a function to read the backtest and chart for individual stocks
# stock chart vs moving averages & showing entry exit points or somehting.
