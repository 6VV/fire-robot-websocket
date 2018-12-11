#!/usr/bin/env python
# -*-coding: utf-8 -*-

'''
服务器接收客户端数据并向机器人传输
'''

import asyncio
import websockets
from module import remote
import zmq


class InfoController(object):
    def start(self):
        self.start_server_to_client()

    def start_server_to_client(self):
        socket: zmq.Socket = remote.get_pub_socket(port=20000)

        async def do(websocket, path):
            while True:
                data = await websocket.recv()
                socket.send_string(data)
                # print(data)

        start_server = websockets.serve(do, '0.0.0.0', 5700)
        asyncio.get_event_loop().run_until_complete(start_server)
