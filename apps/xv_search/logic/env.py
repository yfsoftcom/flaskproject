# -*- coding: utf-8 -*-
import os
import logging
from libs.redis import RedisHelper

USE_PROXY = os.getenv('USE_PROXY', '1')

DOMAIN = 'https://www.xvideos.com'
RSS_URL = DOMAIN + '/rss/rss.xml'

URL = DOMAIN + '/?k='
VIDEO_PREFIX = DOMAIN

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

VIDEO_FRAME = DOMAIN + '/embedframe/'

VERSION = '1.0.0'

logging.debug('USE_PROXY is %s, URL: %s, VIDEO_PREFIX: %s' % (USE_PROXY, URL, VIDEO_PREFIX))

redisHelper = RedisHelper()
redisHelper.connect(REDIS_HOST)

