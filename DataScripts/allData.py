from DataScripts import stockData

# fetch the tickers
tickers = stockData.getTickers('R3000')

# get data for those tickers
r3000Data = stockData.getIndexData(fileName='R3000Data', update=False)
