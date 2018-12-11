#!/usr/bin/env python
# -*-coding: utf-8 -*-

'''
此代码已废弃
'''

import asyncio
import websockets
from module import remote
import zmq


class FireBranchController(object):
    def start(self):
        socket: zmq.Socket = remote.get_pub_socket(port=20004)

        async def do(websocket, path):
            while True:
                data = await websocket.recv()
                socket.send_string(data)
                # print(data)
                # with open('car.jpg', 'rb') as f:
                #     await websocket.send(f.read())
                #     await asyncio.sleep(1)

        start_server = websockets.serve(do, '0.0.0.0', 5683)
        asyncio.get_event_loop().run_until_complete(start_server)
