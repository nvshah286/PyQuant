import pandas as pd
import pandas_datareader as pdr
import datetime
import os.path

def getStockData(symbols=None, startDate=None, endDate=None, fileName=None, value ='Adj Close'):
    filePath = 'DataFiles/' + fileName + '.csv'
    if os.path.isfile(filePath):
        stockData = pd.read_csv(filePath)
        stockData.set_index('Date', inplace=True,drop= True)
        stockData.index = pd.to_datetime(stockData.index)
        return stockData
    else:
        if symbols == None:
            listDF = pd.read_csv('DataFiles/SP500Symbols.csv',index_col='Date')
            symbols = listDF.Symbol

        stockData = pd.DataFrame()
        for s in symbols:
            stocks = pdr.get_data_yahoo(s, startDate, endDate)[value]
            stockData = pd.concat([stockData, stocks], axis=1)
            print(s)

        stockData.columns = symbols[:stockData.shape[1]]
        stockData.to_csv(filePath)
        return stockData
