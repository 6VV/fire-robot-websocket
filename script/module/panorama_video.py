#!/usr/bin/env python
# -*-coding: utf-8 -*-

import asyncio
import websockets
import threading
from module import tools
import os
from module import remote
import time


class PanoramaVideo(object):
    def __init__(self):
        self.image = ''
        self.last_save_time = 0
        # self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

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
            current_time = time.time()
            if current_time - self.last_save_time > 5:
                self.save_file(self.image)
                self.last_save_time = current_time

    def save_file(self, data):
        dir_path = '../file/panorama'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file_path = dir_path + '/' + str(tools.current_time()) + '.jpg'

        with open(file_path, 'wb') as f:
            f.write(data)

    # def __frameToImg(self, frame):
    #     frame = cv2.resize(frame, (2048, 1024), interpolation=cv2.INTER_CUBIC)
    #     result, imgencode = cv2.imencode('.jpg', frame, self.encode_param)
    #     data = numpy.array(imgencode)
    #     image = data.tostring()
    #     return image

    def start_server(self):
        async def send_data(websocket, path):
            try:
                while True:
                    await websocket.send(self.image)
                    await asyncio.sleep(0.2)
            except Exception:
                pass

        start_server = websockets.serve(send_data, '0.0.0.0', 5680)
        asyncio.get_event_loop().run_until_complete(start_server)
