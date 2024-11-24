from market_info import *
import pandas as pd
import numpy as np
from logger import logger

def get_current_hot_stocks():
    market = DomesticMarket()
    volumn_ranks = market.get_volumne_ranking()
    df_vol = pd.DataFrame(volumn_ranks['output'])
    price_ranks = market.get_stock_ranking(market_code=DomesticMarket.MarketCode.ALL.value)
    df_price = pd.DataFrame(price_ranks['output'])
    
    stocks_vol = df_vol['mksc_shrn_iscd'].values
    stocks_price = df_price['stck_shrn_iscd'].values
    
    logger.info(f"Stocks with high volumnes : {stocks_vol}")
    logger.info(f"Stocks with most increased prices : {stocks_price}")


    stock_hot = np.intersect1d(stocks_vol, stocks_price).tolist()
    if not len(stock_hot):
        logger.warning("An empty list will be returned")

    return stock_hot 