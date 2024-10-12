# this is account
from connector import Connector
from logger import logger
import os
import requests
import pandas as pd


class Account(Connector):

    __account_no = None 

    @staticmethod
    def __set_account_no():
        Account.__account_no = os.environ["ACCOUNT_NO"]

    def __init__(self, prdt_cd):
        Account.__set_account_no()
        self.prdt_cd = prdt_cd

    def get_full_account(self):
        return (Account.__account_no, self.prdt_cd)

    def __get_current_balance(self):
        url = f"{Connector.base_url}/uapi/domestic-stock/v1/trading/inquire-balance"
        headers = self.form_common_headers(tr_id="TTTC8434R")
        acno, prdt_cd = self.get_full_account()
        payload = { 
            "CANO" : acno, # this should be implemented in account.py
            "ACNT_PRDT_CD" : prdt_cd, # this should be implemented in account.py
            "AFHR_FLPR_YN" : "N",
            "OFL_YN" : "",
            "INQR_DVSN" : "02",
            "UNPR_DVSN" : "N",
            "FUND_STTL_ICLD_YN" : "N",
            "FNCG_AMT_AUTO_RDPT_YN" : "N",
            "PRCS_DVSN" : "00",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": ""
        }
        logger.info(payload)
        response = requests.get(
            url=url,
            headers=headers,
            params=payload
        )
        ret = response.json()
        try:
            output1_df = pd.DataFrame(ret["output1"])
            output2_df = pd.DataFrame(ret["output2"])
            return output1_df, output2_df
        except Exception as e:
            logger.info(ret["msg1"])
            logger.warning(e)
    

    def get_savings(self):
        pass

    