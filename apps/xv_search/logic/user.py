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
        return {'errno': 0, 'userinfo': userinfo }

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

    def favorite(self, username, vid):
        return {'errno': 0}

    def list_favorite(self, username):
        return {'errno': 0}