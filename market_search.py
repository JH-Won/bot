from connector import Connector
from enum import IntEnum
import requests
from logger import logger
import json

class DateScale(IntEnum):
    DAY = 0
    WEEK = 1
    MONTH = 2

class ExchangerCode():
    @classmethod
    def get_description():
        return {
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
        }

class ForeignMarketEngine(Connector):
    
    def __init__(self):
        super().__init__()
    
    def __format_headers(self, tr_id):
        return {
            "Content-Type": "application/json; charset=UTF-8",
            "authorization" : f"Bearer {self.token_dict['access_token']}",
            "appkey" : self._appkey,
            "appsecret" : self._appsecret,
            "tr_id" : tr_id,
            "custtype" : "P"
        }

    def get_historical_price(self, exchanger_code, stock_code, scale, start_from):
        url = f"{Connector.base_url}/uapi/overseas-price/v1/quotations/dailyprice"
        headers = self.__format_headers(tr_id="HHDFS76240000")
        payload = {
            "AUTH" : "",
            "EXCD" : exchanger_code,
            "SYMB" : stock_code,
            "GUBN" : str(scale),
            "BYMD" : start_from,
            "MODP" : "0"
        }
        response = requests.get(
            url=url,
            headers=headers,
            params=payload
        )

        logger.info(response.json())

        
if __name__ == "__main__":
    # this is test
    engine = ForeignMarketEngine()
    engine.get_historical_price("NAS", "TSLA", DateScale.MONTH, "20240724")
