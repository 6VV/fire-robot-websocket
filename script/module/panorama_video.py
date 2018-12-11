#!/usr/bin/env python
# -*-coding: utf-8 -*-

import asyncio
import websockets
import threading
from cv2 import cv2
import numpy
from module import remote


class PanoramaVideo(object):
    def __init__(self):
        self.image = ''
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def start(self):
        self.begin_receive()
        self.start_server()

    def begin_receive(self):
        thread = threading.Thread(target=self.__receive)
        thread.setDaemon(True)
        thread.start()

    def __receive(self):
        socket = remote.get_sub_socket(port=20002)
        while True:
            self.image = socket.recv()

    # def __frameToImg(self, frame):
    #     frame = cv2.resize(frame, (2048, 1024), interpolation=cv2.INTER_CUBIC)
    #     result, imgencode = cv2.imencode('.jpg', frame, self.encode_param)
    #     data = numpy.array(imgencode)
    #     image = data.tostring()
    #     return image

    def start_server(self):
        async def send_data(websocket, path):
            while True:
                await websocket.send(self.image)
                await asyncio.sleep(0.2)

        start_server = websockets.serve(send_data, '0.0.0.0', 5680)
        asyncio.get_event_loop().run_until_complete(start_server)
