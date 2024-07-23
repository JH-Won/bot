import websockets
import asyncio
import requests
import os 
import json
from ws_utils import stockhoka


def get_approval(key, secret):
    """웹소켓 접속키 발급"""
    url = "https://openapi.koreainvestment.com:9443"
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": key,
            "secretkey": secret}
    PATH = "oauth2/Approval"
    URL = f"{url}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    approval_key = res.json()["approval_key"]
    return approval_key

async def test_connect():
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
                print("websocket closing...")
                break
            
            stock_code = '005930'
            hts_id = 'rrotjd36'
            cust_type = 'P'

            tr_id = 'H0STASP0'
            tr_type = '1'
            send_data = f'''{{
                "header": {{ 
                    "approval_key": "{approval_key}",
                    "custtype": "{cust_type}",
                    "tr_type": "{tr_type}",
                    "content-type": "utf-8"
                }},
                "body": {{
                    "input": {{
                        "tr_id": "{tr_id}",
                        "tr_key": "{stock_code}"
                    }}
                }}
            }}'''
            print("sent data, " + send_data)

            await websocket.send(send_data)
            res_data = await websocket.recv()
            print("Recv command is : ", res_data)

            if res_data[0] == '0':
                recvstr = res_data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
                trid0 = recvstr[1]
                if trid0 == "H0STASP0":  # 주식호가tr 일경우의 처리 단계
                    print("#### 주식호가 ####")
                    stockhoka(recvstr[3])

if __name__ == '__main__':
    asyncio.run(test_connect())
