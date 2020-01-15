# -*- coding: utf-8 -*-
import unittest
from libs.redis import RedisHelper
import json

helper = RedisHelper()

class TestRedisHelper(unittest.TestCase):
    """Test RedisHelper"""

    def setUp(self):
        # docker run --name some-redis -d -p "6379:6379" redis
        helper.connect()

    def tearDown(self):
        helper.close()

    def test_set_and_get_data(self):
        res = helper.set_value_str('test', 'foo')
        self.assertTrue(res)
        self.assertEqual('foo', helper.get_value_str('test'))

    

    # def test_zadd_key_new(self):
    #     """zadd_key_new"""
    #     res = helper.zadd_key_new('aaa', {'bob': 'aaa'})
    #     print('\n', res)
    #     self.assertTrue(False)

    # def test_zadd_key(self):
    #     """zadd_key"""
    #     self.assertTrue(False)