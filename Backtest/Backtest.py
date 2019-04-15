import numpy as np
import pandas as pd


# creating backtest class.
# one thing that is fixed is the function argument.. the first argument will always be 'series'

# hiding some methods within the class right now
# only methods visible are return series & summary at this point.

class BackTest:

    def __init__(self, func=None, stockData=None, arguments=None, holdingPeriod=5):
        self.func = func
        self.args = arguments
        self.holdingPeriod = holdingPeriod
        self.allData = stockData
        self.buyPts = self.__buyPoints()
        self.btReturns = self.retSeries()

    # hiding the function at the point
    def __buyPoints(self):
        buyPts = dict()
        symbols = list(self.allData.keys())
        for s in symbols:
            priceData = self.allData[s].iloc[: (self.holdingPeriod * -4), ]
            buyPts[s] = self.func(priceData, *self.args)

        buyPts = pd.DataFrame(buyPts)
        buyPts.fillna(value=False, inplace=True)
        return buyPts

    def __tradeCounts(self):
        buyPts = self.__buyPoints()
        tradect = buyPts.apply(sum, axis=0)
        return tradect

    def __calcReturns(self, s=None, buyPoints=None):
        series = self.allData[s]['Adj Close']
        series.reset_index(drop=True, inplace=True)
        entryPoints = buyPoints[s]
        if np.nansum(entryPoints) > 0:
            entryPoints.reset_index(drop=True, inplace=True)
            entryTime = entryPoints.index[entryPoints]
            exitVal = series[entryTime + self.holdingPeriod]
            entryVal = series[entryTime]
            return list(100 * (exitVal.values / entryVal.values - 1))
        else:
            return [0]


    def retSeries(self):
        symbols = list(self.allData.keys())
        buyPoints = self.__buyPoints()
        aggSeries = dict()
        errorCount = 0
        for s in symbols:
            try:
                aggSeries[s] = self.__calcReturns(s=s, buyPoints=buyPoints)
            except:
                errorCount += 1
        # TODO: put this data in long data format frame.
        # also have to attach other metadata like ticker, sector, invest style for aggregation.
        print('Total securities with erros is : ', errorCount)
        return aggSeries

    def retSeriesFormatter(self):
        return None

    def summary(self):
        allSeries = []
        retData = self.btReturns
        for s in retData:
            allSeries.extend(retData[s])
        allSeries = pd.Series(allSeries)
        posNeg = allSeries >= 0
        df = pd.DataFrame({'Returns': allSeries, 'PosNeg': posNeg})
        summaryDF = df.groupby('PosNeg')['Returns'].agg(['mean', 'std', 'count'])
        winRatio = round(100 * (summaryDF.loc[True, 'count'] / len(df)), ndigits=4)
        avgPosReturn = round(summaryDF.loc[True, 'mean'], ndigits=4)
        avgNegReturn = round(summaryDF.loc[False, 'mean'], ndigits=4)
        avgRetOverall = round(np.nanmean(df.Returns), ndigits=4)
        avgTrades = round(sum(self.__tradeCounts()) / len(self.allData), ndigits=3)

        summary = {'AvgReturn': avgRetOverall,
                   'AvgPositiveReturn': avgPosReturn,
                   'AvgNegativeReturn': avgNegReturn,
                   'WinRatio': winRatio,
                   'AvgTrades': avgTrades
                   }
        return pd.Series(summary)

# write a function to read the backtest and chart for individual stocks
# stock chart vs moving averages & showing entry exit points or somehting.
