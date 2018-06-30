# -*- coding: utf-8 -*-
import unittest
from logic.tech import TechLogic
from libs.kit import *


logic = TechLogic()
class TestTechLogic(unittest.TestCase):

    """Test TestTechLogic"""

    def test_get_data(self):
        data = logic.get_data()
        print(data)
        self.assertEqual(data[0]['teamCnName'], '俄罗斯')