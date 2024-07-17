import requests
import os
import json
from logger import logger

class Connector(object):

    base_url = "https://openapi.koreainvestment.com:9443"
    header = {
        "Content-Type": "application/json; charset=UTF-8"
    }

    def __init__(self):
        self.__appkey = os.environ["APP_KEY"]
        self.__appsecret = os.environ["APP_SECRET"]
        self.token_dict = self.__get_token()

    def __get_token(self):
        url = Connector.base_url + "/oauth2/tokenP"

        payload = {
            "grant_type" : "client_credentials",
            "appkey" : self.__appkey,
            "appsecret" : self.__appsecret
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
                logger.info(f"Auth Token assigned : {ret}")
                return ret
        except Exception as e:
            logger.warning(str(e))

    def __del__(self):
        url = Connector.base_url + "/oauth2/revokeP"

        try:
            payload = {
                "appkey" : self.__appkey,
                "appsecret" : self.__appsecret,
                "token" : self.token_dict['access_token']
            }

            response = requests.post(
                url=url,
                headers=Connector.header,
                data=payload
            )
            ret = response.json()
            logger.info(f"{ret}")
        except Exception as e:
            logger.warning(str(e))
        

if __name__ == "__main__":
    Conn = Connector()

    del Conn