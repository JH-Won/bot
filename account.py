from connector import Connector
from logger import logger
import os
import requests
import pandas as pd


class Account(Connector):

    def __init__(self, cano, is_foreign):
        super().__init__(cano=cano)
        self.is_foreign = is_foreign

    def get_trading_report(self, start_date, end_date, currency='krw'):
        url = f"{Connector.base_url}/uapi/overseas-stock/v1/trading/inquire-period-profit" if self.is_foreign else f"{Connector.base_url}/uapi/domestic-stock/v1/trading/inquire-period-trade-profit"

        headers = self.form_common_headers(
            tr_id = "TTTS3039R" if self.is_foreign else "TTTC8715R",
            custtype = "P"
        )

        payload = {
            "CANO" : self._cano,
            "OVRS_EXCG_CD" : "",
            "ACNT_PRDT_CD" : self._prdt_cd,
            "NATN_CD" : "",
            "CRCY_CD" : "",
            "PDNO" : "",
            "INQR_STRT_DT" : start_date,
            "INQR_END_DT" : end_date,
            "WCRC_FRCR_DVSN_CD" : "02" if currency == 'krw' else "01",
            "CTX_AREA_NK200" : "",
            "CTX_AREA_FK200" : "", 
        } if self.is_foreign else {
            "CANO" : self._cano,
            "SORT_DVSN" : "01",
            "ACNT_PRDT_CD" : self._prdt_cd,
            "PDNO" : "",
            "INQR_STRT_DT" : start_date,
            "INQR_END_DT" : end_date,
            "CBLC_DVSN" : "00",
            "CTX_AREA_NK100" : "",
            "CTX_AREA_FK100" : "",  
        }

        logger.info(f"payload : {payload}")
        response = requests.get(
            url=url,
            headers=headers,
            params=payload
        )
        ret = response.json()
        logger.info(f"{ret["msg1"]}")
        return ret


    def get_current_assets(self, currency='krw'):
        pass