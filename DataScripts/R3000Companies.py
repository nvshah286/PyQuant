import pandas as pd

url = 'https://www.ishares.com/us/products/239714/ishares-russell-3000-etf/1467271812596.ajax?fileType=csv&fileName=IWV_holdings&dataType=fund'
r3000 = pd.read_csv(url, skiprows = 10)

r3000.to_csv('DataFiles/R3000Companies.csv')