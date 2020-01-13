# -*- coding: utf-8 -*-
import os

NET_MODE = os.getenv('NET_MODE', 'CN')
if NET_MODE == 'GLOBAL':
    DOMAIN = 'https://xvideos.com'
    RSS_URL = DOMAIN + '/rss/rss.xml'
else:
    DOMAIN = 'https://xvideos.sexcache.net'
    RSS_URL = DOMAIN + '/rss'

URL = DOMAIN + '/?k='
VIDEO_PREFIX = DOMAIN

VIDEO_FRAME = DOMAIN + '/embedframe/'

VERSION = '1.0.0'

print('NET_MODE is %s, URL: %s, VIDEO_PREFIX: %s' % (NET_MODE, URL, VIDEO_PREFIX))
