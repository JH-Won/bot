import websockets
import asyncio
import requests
import os 
import json

def get_approval(key, secret):
    """웹소켓 접속키 발급"""
    url = 'https://openapi.koreainvestment.com:9443'
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": key,
            "secretkey": secret}
    PATH = "oauth2/Approval"
    URL = f"{url}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    approval_key = res.json()["approval_key"]
    return approval_key

async def connect():
    app_key = os.environ["APP_KEY"]
    app_secret = os.environ["APP_SECRET"]

    approval_key = get_approval(app_key, app_secret)
    print(f"approval_key = {approval_key}")

    url = "ws://ops.koreainvestment.com:21000"
    async with websockets.connect(url, ping_interval=60) as websocket:
        print("Press 0 to exit")
        while True:
            cmd = input()
            if cmd == '0':
                break
    # on developing
    pass 
            


