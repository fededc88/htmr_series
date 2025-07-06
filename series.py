from bs4 import BeautifulSoup
import requests

import pandas as pd

url = 'https://viberc.liverc.com/results/?p=view_race_result&id=6000488'
r = requests.get(url)

#print(r.text)

soup = BeautifulSoup(r.text, 'html.parser')

soup_table = soup.find('table', class_="table table-striped race_result")
#print(soup_table)

titles = [title.text for title in soup_table.find_all('th')[1:14] ]

tbody = soup_table.find('tbody')

data = [[data.text for data in line.find_all('td')] for line in tbody.find_all('tr')]

#print(data)

#print(titles)

df = pd.DataFrame(columns = titles)

for line in data:
    df.loc[len(df)] = line

print(df)



#names = soup_table.find_all('th')
#print(names)
#
#
#names = soup_table.find_all('span', class_ ='driver_name').text
#print(names);

