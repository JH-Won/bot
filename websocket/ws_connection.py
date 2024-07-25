import websockets
import asyncio
import requests
import os 
import json
import sys
from ws_io_utils import limit_orderbook

sys.path.append("D:/python-api/")
from logger import logger


def get_approval(key, secret):
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

async def connect(tr_id, tr_key, tr_type):
    '''
    Connect websocket and send requests for real-time order book.
    '''
    app_key = os.environ["APP_KEY"]
    app_secret = os.environ["APP_SECRET"]
    try:
        hts_id = os.environ["HTS_ID"]
    except:
        logger.warning("hts_id is not written")
        pass

    approval_key = get_approval(app_key, app_secret)

    logger.info(f"approval_key : {approval_key}")

    url = "ws://ops.koreainvestment.com:21000"
    async with websockets.connect(url, ping_interval=60) as websocket:
        print("Press 0 to exit")
        while True:
            cmd = input()
            if cmd == '0':
                print("websocket closing...")
                break
            send_data = f'''{{
                "header": {{ 
                    "approval_key": "{approval_key}",
                    "custtype": "P",
                    "tr_type": "{tr_type}",
                    "content-type": "utf-8"
                }},
                "body": {{
                    "input": {{
                        "tr_id": "{tr_id}",
                        "tr_key": "{tr_key}"
                    }}
                }}
            }}'''
            logger.info(f"sent data : {send_data}")
            await websocket.send(send_data)
            res_data = await websocket.recv()
            logger.info(res_data)
            
            if res_data[0] == '0':
                recvstr = res_data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
                trid0 = recvstr[1]
                if not trid0 == "PINGPONG":
                    print("#### ORDER TABLE ####")
                    limit_orderbook(recvstr[3])

if __name__ == '__main__':
    tr_id = sys.argv[1]
    tr_key = sys.argv[2]
    tr_type = sys.argv[3]

    asyncio.run(connect(
        tr_id=tr_id,
        tr_key=tr_key,
        tr_type=tr_type
    ))
