from connector import Connector
from enum import IntEnum
import requests
from logger import logger

class DateScale(IntEnum):
    DAY = 0
    WEEK = 1
    MONTH = 2

class ExchangerCode():
    @staticmethod
    def view_code():
        print("""
    # 거래소 코드 
    # HKS : 홍콩
    # NYS : 뉴욕
    # NAS : 나스닥
    # AMS : 아멕스
    # TSE : 도쿄
    # SHS : 상해
    # SZS : 심천
    # SHI : 상해지수
    # SZI : 심천지수
    # HSX : 호치민
    # HNX : 하노이
    # BAY : 뉴욕(주간)
    # BAQ : 나스닥(주간)
    # BAA : 아멕스(주간)
    """)
            

class ForeignMarket(Connector):
    
    def __init__(self):
        super().__init__()

    def get_historical_price(self, exchanger_code, ticker, scale, start_from):
        url = f"{Connector.base_url}/uapi/overseas-price/v1/quotations/dailyprice"
        headers = self.form_common_headers(tr_id="HHDFS76240000", custtype="P")
        payload = {
            "AUTH" : "",
            "EXCD" : exchanger_code,
            "SYMB" : ticker,
            "GUBN" : str(scale),
            "BYMD" : start_from,
            "MODP" : "0"
        }
        logger.info(payload)
        response = requests.get(
            url=url,
            headers=headers,
            params=payload
        )

        return response.json()

        
if __name__ == "__main__":
    # this is test
    engine = ForeignMarket()
    engine.get_historical_price("NAS", "TSLA", DateScale.MONTH, "20240724")