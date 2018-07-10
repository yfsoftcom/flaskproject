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

    def test_cache(self):
        logic.do_search('jav bj')
        cache = logic.get_cache('jav bj-0')
        self.assertFalse(cache is False)

    def test_get_video(self):
        vid = '28605129'
        href = 'video28605129-_pov_japanese_blowjob_39_-_from_javz.se'.replace('-', '/')
        data = logic.get_video(vid, href)
        src1 = data['src']
        data = logic.get_video(vid, href)
        src2 = data['src']
        self.assertEqual(src1, src2)

    def test_star(self):
        vid = '28605129'
        href = 'video28605129-_pov_japanese_blowjob_39_-_from_javz.se'.replace('-', '/')
        data = logic.get_video(vid, href)
        star1 = data['star']
        logic.star(vid)
        data = logic.get_video(vid, href)
        star2 = data['star']
        self.assertEqual(star1, star2 - 1)


"""
    def test_get_video(self):
        mp4_url = logic.get_video('http://xvideos.sexcache.net/video12050059/japan_hd_special_japanese_blowjob')
        print(mp4_url)
        # download_file(mp4_url, 'demo.mp4')
        self.assertTrue(str_include('https://video-hw.xvideos-cdn.com/videos/mp4/b/1/9/xvideos.com_b190e77d1dfe475671da7c80311c8cda-1.mp4', mp4_url))
"""

    