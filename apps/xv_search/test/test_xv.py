# -*- coding: utf-8 -*-
import unittest
from libs.kit import *
from logic.search import XvSearchLogic

logic = XvSearchLogic()

class TestXvSearchLogic(unittest.TestCase):

    """Test TestXvSearchLogic"""

    # def test_search(self):
    #     datas = logic.do_search()
    #     print(datas)
    #     self.assertTrue(True)

    def test_get_video(self):
        mp4_url = logic.get_video('http://xvideos.sexcache.net/video12050059/japan_hd_special_japanese_blowjob')
        print(mp4_url)
        # download_file(mp4_url, 'demo.mp4')
        self.assertTrue(str_include('https://video-hw.xvideos-cdn.com/videos/mp4/b/1/9/xvideos.com_b190e77d1dfe475671da7c80311c8cda-1.mp4', mp4_url))

    