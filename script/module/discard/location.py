#!/usr/bin/env python
# -*-coding: utf-8 -*-

'''
此代码已废弃
'''

import time
import zmq
import json
import asyncio
import websockets
import threading
import os
from module import remote


class Location(object):
    def __init__(self):
        self.g_location_data = None
        self.g_socket_ids: set = set()

    def start(self):
        self.begin_receive()
        self.start_server()

    def begin_receive(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.setDaemon(True)
        receive_thread.start()

    def receive(self):
        socket = remote.get_sub_socket(port=20001)

        while True:
            data = socket.recv_json()
            self.g_location_data = json.dumps(data)
            self.g_socket_ids.clear()
            self.save_file(data)

    def start_server(self):
        async def send_data(websocket, path):
            socket_id = id(websocket)
            while True:
                if self.g_location_data is not None and socket_id not in self.g_socket_ids:
                    await websocket.send(self.g_location_data)
                    self.g_socket_ids.add(socket_id)
                await asyncio.sleep(0.0001)

        start_server = websockets.serve(send_data, '0.0.0.0', 5678)
        asyncio.get_event_loop().run_until_complete(start_server)

    def save_file(self, data):
        dir_path = '../file'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file_path = dir_path+'/'+data['date']+'.txt'

        with open(file_path, 'a') as f:
            f.write(data['time']+':')
            f.write(json.dumps(data))
            f.write('\n')
