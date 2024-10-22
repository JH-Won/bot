import sys
import os
import json
import aiofiles

# root path
project_path = 'D:/python-api'
sys.path.append(project_path)

from websocket.ws_io_utils import get_current_time, get_current_day, format_csv_purchased
from websocket.ws_connection import get_approval
import websockets
import asyncio

output_dir = f"{project_path}/output_{get_current_day()}"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

async def accumulate_data_forever():
    tickers = sys.argv[1:]
    print(f'Given tickers : {tickers}')

    # accumulate data
    url = 'ws://ops.koreainvestment.com:21000'

    tr_id = 'H0STCNT0'
    tr_type = '1'

    while True:
        try:
            approval_key = get_approval(os.environ['APP_KEY'], os.environ['APP_SECRET'])
            dead_count = 0
            
            async with websockets.connect(url, ping_interval=30) as ws:
                print("ws (re)connected.")

                while True:

                    if dead_count >= 240:
                        print(f'it seems something wrong.. deaed count : {dead_count}. Reconnect ws...')
                        break

                    for ticker in tickers:       
                        # making request data to send using ticker list 
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
                                                "tr_key": "{ticker}"
                                            }}
                                        }}
                                    }}'''

                        # send data
                        await ws.send(send_data)
                        recv_data = await ws.recv()

                        # response is purchase data 
                        if recv_data[0] == '0' or recv_data[1] == '1':
                            # print(recv_data)
                            recvstr = recv_data.split('|')
                            data_cnt = int(recvstr[2])
                            file_name = f"{output_dir}/{ticker}_{get_current_time()}.csv"
                            async with aiofiles.open(file_name, mode='w', encoding='UTF-8') as f:
                                await f.write(format_csv_purchased(data_cnt, recvstr[3]))
                        # response is subscription
                        else: 
                            dead_count += 1
                            json_data = json.loads(recv_data)
                            tr_id = json_data['header']['tr_id']
                            if tr_id == 'PINGPONG':
                                await ws.pong(recv_data)

                        await asyncio.sleep(0.05)
                    await asyncio.sleep(0.2)

        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    # run forever
    asyncio.get_event_loop().run_until_complete(accumulate_data_forever())
    asyncio.get_event_loop().close()