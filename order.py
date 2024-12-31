from connector import Connector
import requests
import json
from logger import logger

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