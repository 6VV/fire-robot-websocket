#!/usr/bin/env python
# -*-coding: utf-8 -*-

from module.video.abstract_video import AbstractVideo


class FireBranchVideo(AbstractVideo):
    def __init__(self):
        super(FireBranchVideo, self).__init__(
            robot_port=20003, client_port=5679, file_type='fire_branch_video')
