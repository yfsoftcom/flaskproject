# -*- coding: utf-8 -*-
import os, time, re, json
from libs.kit import *
from .env import URL, VIDEO_PREFIX, VIDEO_FRAME, redisHelper

class UserLogic(object):
    def __init__(self):
        self._r = redisHelper
        pass

    def login(self, username, password):
        userinfo = self._r.get_instance().hget("userinfo", username)
        if userinfo is None:
            return {'errno': -1001 }
        userinfo = json.loads(userinfo)
        if password != userinfo['password']:
            return { 'errno': -1002 }
        now = current_milli_time()
        userinfo['loginAt'] = now
        self._r.get_instance().hset("userinfo", username, json.dumps(userinfo))
        return {'errno': 0, 'data': userinfo }

    def register(self, userinfo):
        username = userinfo['username']
        if self._r.get_instance().hexists("userinfo", username):
            return { 'errno': -2001 }
        now = current_milli_time()
        userinfo['salt'] = 'foo'
        userinfo['createAt'] = now
        userinfo['loginAt'] = now
        userinfo['loginIp'] = '127.0.0.1'
        self._r.get_instance().hset("userinfo", username, json.dumps(userinfo))
        return {'errno': 0}

    def favorite(self, username, vid, info):
        info['createAt'] = current_milli_time()
        self._r.get_instance().hset("favorite:" + username , vid, json.dumps(info))
        return {'errno': 0}

    def del_favorite(self, username, vid):
        self._r.get_instance().hdel("favorite:" + username , vid)
        return {'errno': 0}

    def list_favorite(self, username):
        favoriteList = self._r.get_instance().hvals("favorite:" + username)
        favoriteList = list(map(lambda x: json.loads(x), favoriteList))
        return {'errno': 0, 'data': { 'total': len(favoriteList), 'rows': favoriteList } }