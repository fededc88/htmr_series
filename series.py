from bs4 import BeautifulSoup
import requests

import pandas as pd
import argparse


def getargs():

    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    
    parser.add_argument('url',
            type = str,
            help = 'LiveRC race result url')

    return parser.parse_args()

def main():

    args = getargs()

    print(args.url)

    r = requests.get(args.url)
    
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

if __name__ == '__main__':
    main()




