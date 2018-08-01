# -*- coding: utf-8 -*-
import unittest, re
from libs.kit import *
from stock.logic.stock import *

class TestStock(unittest.TestCase):

    """Test """

    # def test_create_table(self):
    #     create_table()
    #     self.assertTrue(True)

    # def test_save_all_stocks(self):
    #     total = save_all_stocks()
    #     self.assertTrue(total > 3000)

    # def test_fetch_stock_hist(self):
    #     # 凯撒旅游 000796.SZ 方大炭素 600516.SH
    #     total, count = fetch_stock_hist(stock_code = ['000796', '600516'], starttime = '2016-01-01', endtime = '2018-07-31')
    #     print('\n', total, count)
    #     self.assertTrue(total == 2 and count > 100)

    def test_get_stock_big_trade(self):
        df = get_stock_big_trade(stock_code = [], day = '2018-07-18')
        print('\n', df)
        self.assertTrue(True)