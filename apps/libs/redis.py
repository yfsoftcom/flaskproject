# -*- coding: utf-8 -*-
"""
its for redis helper
"""

import redis
encoding = 'utf-8'

class RedisHelper(object):
    def __init__(self):
        self._r = None

    def connect(self, host = 'localhost', port = 6379):
        self._r = redis.Redis(host = host, port = port)
    
    def get_instance(self):
        return self._r

    def close(self):
        pass

    def setex(self, key, value, ex):
        """string 设置key value"""
        res = self._r.setex(key, ex, value)
        return res

    def set(self, key, value):
        """string 设置key value"""
        res = self._r.set(key, value)
        return res

    def get(self, key, wrapper = None):
        """string 根据key 获取值 返回True"""
        res = self._r.get(key)
        if res == None:
            return None
        if wrapper != None:
            res = wrapper(res)
        else:
            res = str(res, encoding)
        return res

    def delete(self, key):
        """string 根据key 删除这个键值"""
        res = self._r.delete(key)
        return res

    def exists(self, key):
        """判断指定的key是否存在 存在返回True 否则 False"""
        res = self._r.exists(key)
        return res
    
    def zadd_key_new(self, name, data):
        """
        添加有序集合数据
        :param name:
        :param score:
        :param value:
        :return:
        """
        if isinstance(data, dict):
            res = self._r.zadd(name, **data)
        else:
            res = self._r.zadd(name, *data)
        return res

    def zadd_key(self, name, *args, **kwargs):
        """
        添加有序集合数据
        :param name:
        :param score:
        :param value:
        :return:
        """
        res = self._r.zadd(name, *args, **kwargs)
        return res

    def zrange_key(self, name, start, end, withscores):
        """
        获取数据
        :param name:
        :param start:
        :param end:
        :param withscores:
        :return:
        """
        res = self._r.zrange(name, start, end, withscores=withscores)
        return res

    def zrank_key(self, name, value):
        """
        获取成员one在Sorted-Set中的位置索引值。0表示第一个位置。
        :param name:
        :param value:
        :return:
        """
        res = self._r.zrank(name, value)
        return res

    def zincrby_key(self, name, value, amount):
        """
        提升分数
        :param name:
        :param value:
        :param amount:
        :return:
        """
        res = self._r.zincrby(name, value, amount)
        return res

    def zrangebyscore_key(self, name, min, max, start=None, num=None,
                          withscores=False, ):
        """
        获取分数满足表达式1 <= score <= 2的成员
        :param name:
        :param min:
        :param max:
        :param start:
        :param num:
        :param withscores:
        :return:
        """
        res = self._r.zrangebyscore(name, min, max, start=None, num=None,
                              withscores=False, )
        return res