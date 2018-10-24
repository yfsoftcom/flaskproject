# -*- coding: utf-8 -*-
import requests
import json, time, hashlib
from urllib import parse
from .kit import *
headers = {'Content-Type': 'application/json'}

class FpmException(Exception):
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error
        self.message = error['message']
        self.code = error['code']
        self.errno = error['errno']

    def __str__(self):
        return json.dumps(self.error, ensure_ascii = False)

class Fpmc(object):
    def __init__(self, appkey='123123', masterKey='123123', domain='http://api.yunplus.io'):
        self._appkey = appkey
        self._masterKey = masterKey
        self._domain = domain
        self._ping = domain + '/ping'
        self._api = domain + '/api'

    def ping(self):
        return get_json(self._ping)

    def call_func(self, method, params, v='0.0.1'):
        arg_dict = {
            'appkey': self._appkey,
            'masterKey': self._masterKey,
            'method': method,
            'param': json.dumps(params, ensure_ascii = False),
            'timestamp': current_milli_time(), 
            'v': v
        }
        arr = []
        for (k, v) in arg_dict.items():
            if k == 'param':
                v = parse.quote(v)
            arr.append(k + '=' + str(v))
        content = '&'.join(arr)
        
        sign = md5(content)
        arg_dict['sign'] = sign
        arg_dict.pop('masterKey')
        rst = post_json(self._api, arg_dict)
        if rst['errno'] == 0:
            return rst['data']
        raise FpmException(rst)