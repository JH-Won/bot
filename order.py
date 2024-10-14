from connector import Connector
import requests
import json
from logger import logger
from overrides import overrides
from account import Account

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

    def __init__(self, account : Account):
        account_no, prdt_cd = account.get_full_account()
        self.account_no = account_no
        self.prdt_cd = prdt_cd

    @overrides
    def order(self, ticker : str, quantity : int, price : int, **kwargs):

        isBuy = price > 0
        tr_id = "TTTC0802U" if isBuy else "TTTC0801U"
        order_type = "00" # on quote
        if "order_type" in kwargs.keys():
            order_type = kwargs["order_type"]
    
        url = f"{Connector.base_url}/uapi/domestic-stock/v1/trading/order-cash"
        headers = self.form_common_headers(tr_id=tr_id)
        payload = { 
            "CANO" : self.account_no, 
            "ACNT_PRDT_CD" : self.prdt_cd, 
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
