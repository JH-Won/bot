import sys
import subprocess
import pandas as pd 

# root path
project_path = 'D:/python-api'
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
    
    print(vol_top5, price_top5)

    picked = []
    for vol_code in vol_top5:
        for price_code in price_top5:
            if vol_code == price_code: 
                picked.append(vol_code)
                if len(picked) >= 3: return picked

    assert len(picked) > 0
    return picked


if __name__ == '__main__':

    tickers = get_high_vol_up()
    subprocess.run([
        'python',
        f'{project_path}/websocket/ws_accumulate_data.py ',
    ] + tickers)