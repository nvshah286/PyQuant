import pandas as pd
import pandas_datareader as pdr
import datetime

startDate = datetime.datetime(2013,1,1)
endDate = datetime.datetime(2018,11,1)


def getStockData(symbols = None, startDate = None, endDate = None, fileName = None):
    if symbols == None:
        listDF = pd.read_csv('/Users/nvs/Documents/GitHub/PyQuant/DataFiles/SP500Symbols.csv')
        symbols = listDF.Symbol

    stockData = pd.DataFrame()

    for s in symbols:
        stocks = pdr.get_data_yahoo(s, startDate, endDate)
        pctChange = stocks['Adj Close'].pct_change()
        stockData = pd.concat([stockData,pctChange], axis= 1)
        print(s)

    stockData.columns = symbols[:stockData.shape[1]]
    filePath = 'DataFiles/' + fileName + '.csv'
    stockData.to_csv(filePath)
    return filePath