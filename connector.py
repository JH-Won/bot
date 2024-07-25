import requests
import os
import json
from datetime import datetime
from logger import logger

class Connector(object):

    # static members, should be used as constants
    base_url = "https://openapi.koreainvestment.com:9443"
    header = {
        "Content-Type": "application/json; charset=UTF-8"
    }

    def __init__(self):
        self._appkey = os.environ["APP_KEY"]
        self._appsecret = os.environ["APP_SECRET"]
        self.token_dict = self.__get_token()


    def __is_token_expired(self):
        try:
            with open("token.json", "r") as token_dict:
                token_dict = json.load(token_dict)
                return datetime.now() > datetime.strptime(token_dict["access_token_token_expired"], "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            logger.warning(str(e))
            return False

    def __get_token(self):
        if os.path.exists('./token.json') and (not self.__is_token_expired()):
            with open("token.json", "r") as token_dict:
                return json.load(token_dict)

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
                logger.info(f"Auth Token assigned : {ret}")
                # write a daily token for cache
                with open("token.json", "w") as token_dict:
                    token_dict.write(json.dumps(ret))
                return ret
        except Exception as e:
            logger.warning(str(e))

# This is for test
if __name__ == "__main__":
    Conn = Connector()