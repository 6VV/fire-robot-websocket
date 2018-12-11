#!/usr/bin/env python
# -*-coding: utf-8 -*-

import asyncio
import websockets
import threading
from cv2 import cv2
import numpy
from module import remote


class FireBranchVideo(object):
    def __init__(self):
        self.image = ''
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def start(self):
        self.begin_receive()
        self.start_server()

    def begin_receive(self):
        receive_thread = threading.Thread(target=self.__receive)
        receive_thread.setDaemon(True)
        receive_thread.start()

    def __receive(self):
        socket = remote.get_sub_socket(port=20003)
        while True:
            self.image = socket.recv()

    def start_server(self):
        async def send_data(websocket, path):
            while True:
                await websocket.send(self.image)
                await asyncio.sleep(0.2)

        start_server = websockets.serve(send_data, '0.0.0.0', 5679)
        asyncio.get_event_loop().run_until_complete(start_server)
