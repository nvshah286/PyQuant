import numpy as np
import pandas as pd


# creating backtest class.
class BackTest:

    def __init__(self, func=None, stockData=None, arguments=None, holdingPeriod=5):
        self.func = func
        self.args = arguments
        self.holdingPeriod = holdingPeriod
        self.testData = stockData.iloc[: -40, ]

    def buyPoints(self):
        buyPts = self.testData.apply(func=self.func, args=self.args, axis=0)
        return buyPts

    def tradeCounts(self):
        buyPts = self.buyPoints()
        tradeCounts = buyPts.apply(sum, axis=0)
        return tradeCounts

    def calcReturns(self, series=None, entryPoints=None):
        entryPoints.reset_index(drop=True, inplace=True)
        series.reset_index(drop=True, inplace=True)
        entryTime = entryPoints.index[entryPoints]
        exitVal = series[entryTime + self.holdingPeriod]
        entryVal = series[entryTime]
        return 100 * (exitVal.values / entryVal.values - 1)

    def retSeries(self):
        aggSeries = []
        for s in self.testData.columns:
            returns = self.calcReturns(series=self.testData[s],
                                       entryPoints=self.buyPoints()[s])
            aggSeries.append(returns)
        aggSeries = pd.Series(aggSeries)
        aggSeries.index = self.testData.columns
        return aggSeries

    def summary(self):
        allSeries = pd.Series()
        for s in self.retSeries():
            allSeries = pd.concat([allSeries, pd.Series(s)], axis=0)
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
