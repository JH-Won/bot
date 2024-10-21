import sys
import time
import json
import pandas as pd 
from tabulate import tabulate

# root path
project_path = 'D:/python-api'
sys.path.append(project_path)

from market_info import DomesticMarket
from logger import logger

if __name__ == '__main__':
    market = DomesticMarket()

    while True:
        # ranks = market.get_stock_ranking(market_code=DomesticMarket.MarketCode.ALL.value)
        ranks = market.get_volumne_ranking()
        try:
            output = ranks['output']
            # logger.info(output)
            df = pd.DataFrame(output)
            print(tabulate(df, headers='keys', tablefmt='psql'))
            time.sleep(0.3)
        except Exception as e:
            logger.warning(e)



    