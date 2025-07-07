import logging
from bs4 import BeautifulSoup
import requests

import pandas as pd
import argparse

logger = logging.getLogger(__name__)

def getargs():

    parser = argparse.ArgumentParser(
                    prog='scrapercres',
                    description='LiveRC race results web scraper',
                    epilog='All kind of submissions are welcome. (fededc88@gmail.com')
    
    parser.add_argument('url',
            metavar = 'URL',
            type = str,
            help = 'LiveRC race result url')

    parser.add_argument('-o', '--output',
            metavar = 'output',
            type = str,
            default = None,
            help = '.CSV output file')

    parser.add_argument('-v', '--verbose',
            metavar = 'verbose',
            type = str,
            default = 'INFO',
            choices = ['CRITICAL', 'DEBUG', 'ERROR', 'FATAL', 'INFO', 'NOTSET'],
            help = '.CSV output file')

    return parser.parse_args()

def main():

    args = getargs()

    logging.basicConfig(level=args.verbose)

    try:
        logger.info(f"requesting: {args.url}")
        r = requests.get(args.url)
        logger.debug(r.text)
    except Exception as e:
        logger.error(e)
        exit(-1)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    soup_table = soup.find('table', class_="table table-striped race_result")
    logger.debug(soup_table)
    
    titles = [title.text for title in soup_table.find_all('th')[1:14] ]
    logger.debug(titles)
    
    tbody = soup_table.find('tbody')
    data = [[data.text for data in line.find_all('td')] for line in tbody.find_all('tr')]
    logger.debug(data)
    
    df = pd.DataFrame(columns = titles)
    
    for line in data:
        df.loc[len(df)] = line
    
    logger.info(df)

    if args.output:
        df.to_csv(args.output, index=False)

if __name__ == '__main__':
    main()




