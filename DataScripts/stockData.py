import pandas as pd
import pandas_datareader as pdr
import datetime
import os.path


def getStockData(symbols=None, startDate=None, endDate=None, fileName=None, value='Adj Close'):
    filePath = 'DataFiles/' + fileName + '.csv'
    if os.path.isfile(filePath):
        stockData = pd.read_csv(filePath)
        # stockData.set_index('Date', inplace=True,drop= True)
        # stockData.index = pd.to_datetime(stockData.index)
        return stockData
    else:
        if symbols == None:
            listDF = pd.read_csv('DataFiles/SP500Companies.csv')
            symbols = listDF.Symbol

        stockData = pd.DataFrame()
        for s in symbols:
            stocks = pdr.get_data_yahoo(s, startDate, endDate)[value]
            stockData = pd.concat([stockData, stocks], axis=1)
            print(s)

        stockData.columns = symbols[:stockData.shape[1]]
        stockData.to_csv(filePath)
        return stockData


def getTickers(index='SP500', sector='Information Technology'):
    if index == 'SP500':
        companies = pd.read_csv('DataFiles/SP500Companies.csv')
        symbols = companies[companies['GICS Sector'] == sector].Symbol
        return symbols
    elif index == 'R3000':
        companies = pd.read_csv('DataFiles/R3000Companies.csv')
        symbols = companies[companies['Sector'] == sector].Ticker
        return symbols
    else:
        exit('Index can be either SP500 or R3000 !')
