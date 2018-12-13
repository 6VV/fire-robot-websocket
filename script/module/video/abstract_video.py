#!/usr/bin/env python
# -*-coding: utf-8 -*-

import threading
import time
import os
import asyncio
import websockets
from module import remote, tools


class AbstractVideo:
    def __init__(self, robot_port, client_port, file_type):
        self.robot_port = robot_port
        self.client_port = client_port
        self.file_type = file_type
        self.image = ''
        self.last_save_time = 0

    def start(self):
        self.begin_receive()
        self.start_server()

    def begin_receive(self):
        thread = threading.Thread(target=self.__receive)
        thread.setDaemon(True)
        thread.start()

    def __receive(self):
        socket = remote.get_sub_socket(port=self.robot_port)
        while True:
            self.image = socket.recv()
            current_time = time.time()
            if current_time - self.last_save_time > 5:
                self.save_file(self.image)
                self.last_save_time = current_time

    def save_file(self, data):
        dir_path = '../file/' + self.file_type
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file_path = dir_path + '/' + str(tools.current_time()) + '.jpg'

        with open(file_path, 'wb') as f:
            f.write(data)

    def start_server(self):
        async def send_data(websocket, path):
            try:
                while True:
                    await websocket.send(self.image)
                    await asyncio.sleep(0.2)
            except Exception:
                pass

        start_server = websockets.serve(send_data, '0.0.0.0', self.client_port)
        asyncio.get_event_loop().run_until_complete(start_server)
