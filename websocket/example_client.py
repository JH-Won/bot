import asyncio
import websockets

async def connect(url):
    async with websockets.connect(url) as websocket:
        print("Press 0 to exit")
        while True:
            cmd = input()
            if cmd == "0":
                break 
            
            await websocket.send(cmd)
            res = await websocket.recv()
            print(res)

        await websocket.close()

if __name__ == "__main__":
    url = "ws://localhost:3300"
    asyncio.get_event_loop().run_until_complete(connect(url))
    print("websocket connection closed")