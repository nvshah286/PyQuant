import pandas as pd
import pandas_datareader as pdr
import datetime
import os.path
import pickle


def getIndexData(symbols=None, startDate=None, endDate=None, fileName=None, update=True):
    filePath = 'DataFiles/' + fileName + '.pickle'
    if os.path.isfile(filePath) and not update:
        print('File already exists so loading from the data')
        with open(filePath, 'rb') as f:
            stockData = pickle.load(f)
        return stockData
    else:
        print('Creating new File with the symbols provided')
        stockData = dict()
        for s in symbols:
            stockData[s] = pdr.get_data_yahoo(s, startDate, endDate)
            print(s)
        with open(filePath, 'wb') as f:
            pickle.dump(stockData, f, pickle.HIGHEST_PROTOCOL)
        return stockData


def getTickers(index='SP500', sector='Information Technology'):
    if index == 'SP500':
        companies = pd.read_csv('DataFiles/SP500Companies.csv')
        if sector is None:
            symbols = companies.Symbol
        else:
            symbols = companies[companies['GICS Sector'] == sector].Symbol
        return symbols
    elif index == 'R3000':
        companies = pd.read_csv('DataFiles/R3000Companies.csv')
        if sector is None:
            symbols = companies.Ticker
        else:
            symbols = companies[companies['Sector'] == sector].Ticker
        return symbols
    else:
        exit('Index can be either SP500 or R3000 !')
