from connector import Connector
from enum import IntEnum
import requests
import json
from logger import logger
from overrides import overrides


class OrderType(IntEnum):
    on_quote : 0 # 
    on_market : 1 # 


class OrderInterface(Connector):
    '''
    An interface for implementing order service. Any order class has to follow the spec of this interface.
    '''

    def __init__(self):
        super().__init__()

    def order(self, ticker : str, quantity : int, price : int, **kwargs):
        pass

    def list_orders(self):
        pass

    def cancle(self, order_no : str):
        pass
    

class DomesticMarket(OrderInterface):

    @overrides
    def order(self, ticker : str, quantity : int, price : int, **kwargs):

        isBuy = price > 0
        tr_id = "TTTC0802U" if isBuy else "TTTC0801U"
        order_type = "00" # on quote
    
        url = f"{Connector.base_url}/uapi/domestic-stock/v1/trading/order-cash"
        headers = self.form_common_headers(tr_id=tr_id)
        payload = { 
            "CANO" : "", # this should be implemented in account.py
            "ACNT_PRDT_CD" : "", # this should be implemented in account.py
            "PDNO" : ticker,
            "ORD_DVSN" : order_type,
            "ORD_QTY" : str(quantity),
            "ORD_UNPR" : str(abs(price))
        }
        logger.info(payload)
        response = requests.post(
            url=url,
            headers=headers,
            params=payload
        )
        logger.info(response.json())

    @overrides 
    def list_orders(self):
        pass

    @overrides
    def cancle(self, order_no : str):
        pass


class ForeignMarket(OrderInterface):
    pass
