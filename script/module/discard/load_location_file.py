'''
此代码已废弃
'''

import asyncio
import websockets
from jsonrpcserver.aio import methods
import time


async def main(websocket, path):
    # request = await websocket.recv()
    # response = await methods.dispatch(request)
    # if not response.is_notification:
    fo = open("file/18-9-21.txt", "r")
    lines = fo.readlines()
    for line in lines:
        if line.find('"lat_raw": -0.0, "lon_raw": -0.0,') > 0:
            continue
        pos = line.find(':')+1
        line = line[pos:]
        time.sleep(0.02)
        print(line)
        await websocket.send(str(line))

print("server start: 5678")
start_server = websockets.serve(main, '0.0.0.0', 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
