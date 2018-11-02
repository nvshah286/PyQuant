from lxml import html
import requests
import pandas as pd

page = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
tree = html.fromstring(page.content)

table = tree.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody')

table = table[0]
rows = table.findall('tr')
rows = rows[1:]
cellsAr = []

for x in rows:
    cells = x.findall('td')
    cells = [x.text_content() for x in cells]
    cellsAr.append(cells)
df = pd.DataFrame(cellsAr)
df.columns =['Symbol', 'Security','SEC Filings','GICS Sector',' GICS Sub Industry', 'Location','Date Added','CIK','Founded']

listDF = df.loc[:,['Symbol', 'Security','GICS Sector',' GICS Sub Industry', 'Location']]
listDF.to_csv("DataFiles/SP500Symbols.csv")