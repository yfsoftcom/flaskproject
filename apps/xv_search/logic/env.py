# -*- coding: utf-8 -*-
import os
import logging

NET_MODE = os.getenv('NET_MODE', 'GLOBAL')
if NET_MODE == 'GLOBAL':
    DOMAIN = 'https://www.xvideos.com'
    RSS_URL = DOMAIN + '/rss/rss.xml'
else:
    DOMAIN = 'https://xvideos.sexcache.net'
    RSS_URL = DOMAIN + '/rss'

URL = DOMAIN + '/?k='
VIDEO_PREFIX = DOMAIN

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

VIDEO_FRAME = DOMAIN + '/embedframe/'

VERSION = '1.0.0'

logging.debug('NET_MODE is %s, URL: %s, VIDEO_PREFIX: %s' % (NET_MODE, URL, VIDEO_PREFIX))
