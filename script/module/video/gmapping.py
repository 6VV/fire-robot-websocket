#!/usr/bin/env python
# -*-coding: utf-8 -*-

from module.video.abstract_video import AbstractVideo


class GMapping(AbstractVideo):
    def __init__(self):
        super(GMapping, self).__init__(
            robot_port=20004, client_port=5681, file_type='map')
