#!/usr/bin/env python
# -*-coding: utf-8 -*-

import sys
try:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except Exception:
    pass
import asyncio
import websockets
import threading
from module import remote


class GMapping(object):
    def __init__(self):
        self.image = ''

    def start(self):
        self.begin_receive()
        self.start_server()

    def begin_receive(self):
        receive_thread = threading.Thread(target=self.__receive)
        receive_thread.setDaemon(True)
        receive_thread.start()

    def start_server(self):
        async def send_data(websocket, path):
            while True:
                await websocket.send(self.image)
                await asyncio.sleep(0.2)

        start_server = websockets.serve(send_data, '0.0.0.0', 5681)

        asyncio.get_event_loop().run_until_complete(start_server)

    def __receive(self):
        socket = remote.get_sub_socket(port=20004)
        while True:
            self.image = socket.recv()
