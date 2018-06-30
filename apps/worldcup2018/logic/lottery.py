# -*- coding: utf-8 -*-
import os, time, re
from libs.kit import *
from lxml import etree

URL = 'http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47&type=jcmini'

class LotteryLogic(object):
    def __init__(self):
        pass

    def fetch_info(self):
        html = download(URL)
        self._root = etree.ElementTree(etree.HTML(html).xpath('//div[@id="dcc"]')[0])
        self._data = []
        list_tr = self._root.xpath('//tr[@dg="1"]')
        for i, tr in enumerate(list_tr):
            clz = tr.get('class')
            if str_include('hide', clz):
                continue
            if tr.get('m') == '世界杯':
                tr_tree = etree.ElementTree(tr)
                host = tr_tree.xpath('//td[@class="wh-4 t-r"]/a/@title')[0]
                guest = tr_tree.xpath('//td[@class="wh-6 t-l"]/a/@title')[0]
                points = tr_tree.xpath('//td[@class="wh-8 b-l"]/div[1]/a')
                win_point = points[0].text
                equal_point = points[1].text
                fail_point = points[2].text
                self._data.append([host, guest, float(win_point), float(equal_point), float(fail_point), i])

    def get_point(self, match):
        g = match['G']
        h = match['H']
        for data in self._data:
            a = data[0]
            b = data[1]
            win = data[2]
            equal = data[3]
            fail = data[4]
            if a == h and b == g:
                return [win, equal, fail]
            if a == g and b == h:
                return [fail, equal, win]

        return False
                
    def calc_return(self):

        pass

