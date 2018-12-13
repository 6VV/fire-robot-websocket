#!/usr/bin/env python
# -*-coding: utf-8 -*-

from module.video.gmapping import GMapping
from module.video.fire_branch_video import FireBranchVideo
from module.video.panorama_video import PanoramaVideo
from module.info_controller import InfoController
from module.info_server_to_client import InfoServerToClient

import asyncio

if __name__ == '__main__':
    GMapping().start()
    FireBranchVideo().start()
    PanoramaVideo().start()
    InfoController().start()
    InfoServerToClient().start()

    asyncio.get_event_loop().run_forever()
