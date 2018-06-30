# -*- coding: utf-8 -*-
import unittest
from logic.lottery import LotteryLogic
from libs.kit import *


logic = LotteryLogic()
logic.fetch_info()
class TestLotteryLogic(unittest.TestCase):

    """Test TestLotteryLogic"""

    def test_get_point(self):
        points = logic.get_point({'H':'巴西','G':'哥斯达黎加'})
        self.assertEqual(1.08, points[0])