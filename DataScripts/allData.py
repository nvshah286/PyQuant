import datetime
import pandas_datareader as pdr
from DataScripts import stockData
import pickle

startDate = datetime.datetime(2013, 1, 1)
endDate = datetime.datetime.now()
symbols = stockData.getTickers('R3000', None)
allDataDict = {}
for s in symbols:
    print(s)
    stocks = pdr.get_data_yahoo(s, startDate, endDate)
    allDataDict.update({s: stocks})

## saving the file using pickle

with open('DataFiles/R3000Data.pickle', 'wb') as f:
    pickle.dump(allDataDict, f, pickle.HIGHEST_PROTOCOL)

with open('stockData.pickle', 'rb') as f:
    stockList = pickle.load(f)
