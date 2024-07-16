import requests
import os
import json

class Connector(object):

    base_url = "https://openapi.koreainvestment.com:9443"
    header = {
        "Content-Type": "application/json"
    }

    def __init__(self):
        self.__appkey = os.environ["APP_KEY"]
        self.__appsecret = os.environ["APP_SECRET"]
        self.__token = self.__get_token()

    def __get_token(self):
        url = Connector.base_url + "/oauth2/tokenP"

        payload = {
            "grant_type" : "client_credentials",
            "appkey" : self.__appkey,
            "appsecret" : self.__appsecret
        }

        response = requests.post(
            url=url,
            headers=Connector.header,
            data=json.dumps(payload)
        )

        return response.json() if response.status_code == 200 else None
            
    def __del__(self):
        url = Connector.base_url + "/oauth2/revokeP"

        payload = {
            "grant_type" : "client_credentials",
            "appkey" : self.__appkey,
            "appsecret" : self.__appsecret
        }

        response = requests.post(
            url=url,
            headers=Connector.header,
            data=payload
        )
        

if __name__ == "__main__":
    Conn = Connector()

    del Conn
    # import gc
    # gc.collect()
    