# -*- coding: utf-8 -*-
import tushare as ts
import unittest, re
from libs.kit import *

class TestMovie(unittest.TestCase):

    """Test """

    def test_get_realtime_movie(self):
        df = ts.realtime_boxoffice()
        print('\n')
        print(df)
        self.assertTrue(True)


    def test_get_k_data(self):
        e = ts.get_k_data('000796',start='2018-07-23',end='2018-08-31')
        print('\n', e)
        self.assertTrue(True)

    def test_get_realtime_quotes(self):
        df = ts.get_realtime_quotes('000796')
        print('\n', df)
        self.assertTrue(True)