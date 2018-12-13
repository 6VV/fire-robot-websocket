#!/usr/bin/env python
# -*-coding: utf-8 -*-

from module.video.abstract_video import AbstractVideo


class PanoramaVideo(AbstractVideo):
    def __init__(self):
        super(PanoramaVideo, self).__init__(
            robot_port=20002, client_port=5680, file_type='panorama')
