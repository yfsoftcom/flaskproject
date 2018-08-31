# -*- coding: utf-8 -*-
import os, time, re, json
from libs.kit import *
from lxml import etree
from .env import URL, VIDEO_PREFIX, RSS_URL, NET_MODE, DOMAIN

from urllib.request import urlopen
from xml.etree.ElementTree import parse

# 
VALIDE_TIME = 60 * 60 * 10

class XvRssLogic(object):
    def __init__(self):
        self._last_feed_time = None
        self._data = None

    def parse(self):
        NOW = current_milli_time()
        if self._last_feed_time is not None:
            if self._last_feed_time + VALIDE_TIME > NOW:
                return self._datas
        
        xml = download(RSS_URL)
        u = urlopen(RSS_URL)
        doc = parse(u)
        self._datas = []
        for item in doc.iterfind('channel/item'):
            title = item.findtext('title')
            link = item.findtext('link').strip(DOMAIN)
            guid = item.findtext('guid')
            rate = item.findtext('rate')
            thumb = item.findtext('thumb_medium')
            duration = item.findtext('clips/duration')
            self._datas.append({ 'title': title, 'link': link, 'short_href': link.strip('/').replace('/', '-'), 'id': guid, 'rate': rate, 'thumb': thumb, 'duration': duration})
        self._last_feed_time = NOW
        return self._datas
