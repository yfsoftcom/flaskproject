# -*- coding: utf-8 -*-
import unittest
from libs.kit import *
from lxml import etree

class TestKit(unittest.TestCase):
    """Test libs.kit.py"""

    def test_current_milli_time(self):
        """Test method current_milli_time() should after [2018-06-13 09:06:19] = 1528851979"""
        self.assertLess(1528851979, current_milli_time())

    def test_time_format(self):
        """Test method time_format(1528851979) = '2018-06-13 09:06:19'""" 
        self.assertEqual('2018-06-13 09:06:19', time_format(1528851979))

    def test_str_include(self):
        """ str_include """
        self.assertTrue(str_include('123', '#fhdajkf123fda'))
        self.assertFalse(str_include('123', '#fhdajkf1a23fda'))

    def test_write_json(self):
        """ test_write_json """
        flag, e = write_json_to_file('session', {'a': 1})
        self.assertTrue(flag)
        if not flag:
            print(e)
        remove_file('session')

    # def test_get_json(self):
    #     """ test_get_json """
    #     flag, e = write_json_to_file('session', {'a': 1})
    #     data, e = get_json_from_file('session')
    #     self.assertTrue(e==None)
    #     self.assertEqual(1, data['a'])
    #     remove_file('session')

    # def test_download(self):
    #     html = download('http://saishi.zgzcw.com/soccer/cup/75')
    #     dom = etree.HTML(html)
    #     self.assertEqual('2018 世界杯分组赛积分榜', dom.xpath('//*[@id="tabs0_main_1"]/div[1]/div/span/text()')[0])

    def test_get_text(self):
        html = get_text('https://www.xvideos.com')
        self.assertTrue(True)
