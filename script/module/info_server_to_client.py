#!/usr/bin/env python
# -*-coding: utf-8 -*-
'''
服务器接收机器人数据并向客户端传输
'''

import time
import zmq
import json
import asyncio
import websockets
import threading
import os
from module import remote


class Controller(object):
    '''
    管理服务器推送到客户端的数据传输
    避免重复向同一客户端发送同一数据
    '''

    def __init__(self):
        self.g_socket_ids: set = set()

    def on_receive(self, data):
        self.data = data
        self.g_socket_ids.clear()

    def is_ready(self, id):
        '''
        判断是否已向该id对应的socket发送数据
        '''
        if id not in self.g_socket_ids:
            self.g_socket_ids.add(id)
            return True
        return False

    def get_data(self):
        return self.data


class LocationController(Controller):
    def on_receive(self, data):
        super().on_receive(data)
        self.save_file(data)

    def save_file(self, data):
        json_data = json.loads(data)
        dir_path = '../file/location'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        file_path = dir_path + '/' + json_data['date'] + '.txt'

        with open(file_path, 'a') as f:
            f.write(json_data['time'] + ':')
            f.write(data)
            f.write('\n')


class InfoServerToClient(object):
    def __init__(self):
        self.data = None
        self.json_data = None
        self.location_controller = LocationController()

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
            self.data = socket.recv_string()
            self.json_data = json.loads(self.data)

            # TODO:on_receive
            if self.json_data['data']['type'] == 'location':
                self.location_controller.on_receive(
                    self.json_data['data']['data'])

    def start_server(self):
        async def send_data(websocket, path):
            socket_id = id(websocket)
            while True:
                if self.data is not None:
                    # TODO: send
                    if self.location_controller.is_ready(socket_id):
                        await websocket.send(
                            json.dumps(self.json_data['data']))
                await asyncio.sleep(0.001)

        start_server = websockets.serve(send_data, '0.0.0.0', 5701)
        asyncio.get_event_loop().run_until_complete(start_server)
