import requests
import os
import json
from datetime import datetime
from logger import logger
from system_utils import get_init_path

AUTH_JSON_PATH = f"{get_init_path()}/auth.json"


def get_all_accounts():
    with open(AUTH_JSON_PATH, "r") as f:
        key_json =  json.load(f)
        return key_json["ACCOUNTS"]

def get_connection_key(cano):
    accounts = get_all_accounts()
    return next(filter(lambda item: item["CANO"] == cano, accounts), None)


class Connector(object):

    # static members, should be used as constants
    base_url = "https://openapi.koreainvestment.com:9443"
    token_path = f'{get_init_path()}/token.json'
    header = {
        "Content-Type": "application/json; charset=UTF-8"
    }

    def __init__(self, cano):
        account_key = get_connection_key(cano)
        self._cano = cano
        self._prdt_cd = account_key["PRDT_CD"]
        self._appkey = account_key["APP_KEY"]
        self._appsecret = account_key["APP_SECRET"]
        self.token_dict = account_key["TOKEN"] 
        if (not self.token_dict) or (datetime.now() > datetime.strptime(self.token_dict["access_token_token_expired"], "%Y-%m-%d %H:%M:%S")):
            self.token_dict = self.__get_new_token()

    def __get_new_token(self):
        url = Connector.base_url + "/oauth2/tokenP"

        payload = {
            "grant_type" : "client_credentials",
            "appkey" : self._appkey,
            "appsecret" : self._appsecret
        }
        try:
            response = requests.post(
                url=url,
                headers=Connector.header,
                data=json.dumps(payload)
            )
            ret = response.json() 
            if "error_description" in ret:
                logger.warning(ret["error_description"])
            else:
                # write a daily token for cache
                with open(AUTH_JSON_PATH, "r") as f:
                    data = json.load(f)
                for item in data["ACCOUNTS"]:
                    if item["CANO"] == self._cano:
                        item["TOKEN"] = ret 
                        break
                with open(AUTH_JSON_PATH, "w") as f:
                    json.dump(data, f, indent=4)
                
                logger.info(f"Auth token successfully assigned and cached")

                return ret
        except Exception as e:
            logger.warning(str(e))
    
    def form_common_headers(self, **kwargs):
        return {
            "Content-Type": "application/json; charset=UTF-8",
            "authorization" : f"Bearer {self.token_dict['access_token']}",
            "appkey" : self._appkey,
            "appsecret" : self._appsecret,
        } | kwargs

# This is for test
if __name__ == "__main__":
    Conn = Connector("81263805")
    print(Conn.form_common_headers())