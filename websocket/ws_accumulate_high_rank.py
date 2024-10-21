import sys
import subprocess
import pandas as pd 
from tabulate import tabulate

# root path
project_path = 'E:/bot'
sys.path.append(project_path)

from market_info import DomesticMarket
from logger import logger

def get_high_vol_up():
    market = DomesticMarket()
    volumn_ranks = market.get_volumne_ranking()
    df_vol = pd.DataFrame(volumn_ranks['output'])
    price_ranks = market.get_stock_ranking(market_code=DomesticMarket.MarketCode.ALL.value)
    df_price = pd.DataFrame(price_ranks['output'])
    
    vol_top5 = df_vol['mksc_shrn_iscd'].values[:5]
    price_top5 = df_price['stck_shrn_iscd'].values[:5]
    
    picked = None
    for vol_code in vol_top5:
        for price_code in price_top5:
            if vol_code == price_code: 
                picked = vol_code
                return picked
    assert picked is not None


if __name__ == '__main__':
    ticker = get_high_vol_up()
    subprocess.run([
        'python',
        f'{project_path}/websocket/ws_accumulate_data.py',
        ticker
    ])
