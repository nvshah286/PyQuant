import pandas as pd
import pandas_datareader as pdr
import datetime

startDate = datetime.datetime(2013,1,1)
endDate = datetime.datetime(2018,11,1)


index = pdr.get_data_yahoo("SPY", startDate, endDate)['Adj Close']
oil = pdr.fred.FredReader("DCOILWTICO", startDate, endDate).read()
gold = pdr.fred.FredReader("GOLDAMGBD228NLBM", startDate, endDate).read()
naturalGas = pdr.fred.FredReader("DHHNGSP", startDate, endDate).read()

macrodata = pd.concat([index, oil, gold,naturalGas],axis=1)
macrodata.columns = ['SP500','Oil','Gold','NaturalGas']
macrodata = macrodata.pct_change()

macrodata.to_csv('DataFiles/MacroData.csv')