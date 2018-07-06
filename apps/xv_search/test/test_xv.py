# -*- coding: utf-8 -*-
import unittest
# from libs.kit import *
from xv_search.logic.search import XvSearchLogic

logic = XvSearchLogic()

class TestXvSearchLogic(unittest.TestCase):

    """Test TestXvSearchLogic"""

    def test_search(self):
        logic.do_search('jav bj')
        logic.do_search('jav bj')
        logic.do_search('jav ass')
        logic.do_search('jav ass')
        logic.do_search('jav bj')
        self.assertEqual(logic.get_top3_keywords()[0], 'jav bj')
        self.assertEqual(logic.get_top3_keywords()[1], 'jav ass')
        logic.do_search('jav bj', 1)
        logic.do_search('jav bj', 2)
        logic.do_search('jav bj', 3)
        logic.do_search('jav ass')
        logic.do_search('jav ass')
        self.assertEqual(logic.get_top3_keywords()[0], 'jav bj')

"""
    def test_get_video(self):
        mp4_url = logic.get_video('http://xvideos.sexcache.net/video12050059/japan_hd_special_japanese_blowjob')
        print(mp4_url)
        # download_file(mp4_url, 'demo.mp4')
        self.assertTrue(str_include('https://video-hw.xvideos-cdn.com/videos/mp4/b/1/9/xvideos.com_b190e77d1dfe475671da7c80311c8cda-1.mp4', mp4_url))
"""

    