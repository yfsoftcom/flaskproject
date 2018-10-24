# -*- coding: utf-8 -*-
import unittest
from libs.fpmc import *
from lxml import etree

class TestFpmc(unittest.TestCase):
    """Test libs.fpmc.py"""

    def test_func(self):
        """Test method """
        fpm = Fpmc()
        try:
            print(fpm.ping())
            data = fpm.call_func('system.show',{ }) 
            print (data)
        except FpmException as e:
            print (e)