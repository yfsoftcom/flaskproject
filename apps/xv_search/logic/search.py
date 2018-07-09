# -*- coding: utf-8 -*-
import os, time, re
from operator import itemgetter, attrgetter
from libs.kit import *
from lxml import etree

URL = 'http://xvideos.sexcache.net/?k='
VIDEO_PREFIX = 'http://xvideos.sexcache.net'

"""
<div id="video_34542905" class="thumb-block ">
    <div class="thumb-inside">
        <div class="thumb">
            <a href="/video34542905/mothers_fucked_in_front_of_their_daughters">
            <img src="https://static-hw.xvideos.works/img/lightbox/lightbox-blank.gif" 
                data-src="https://img-hw.xvideos-cdn.com/videos/thumbs169/1e/97/ac/1e97ac3658a6b68618e57843209e7c91/1e97ac3658a6b68618e57843209e7c91.21.jpg"
                data-idcdn="2" 
                data-videoid="34542905" 
                id="pic_34542905" />
            </a>
        </div>
    </div>
    <p>
        <a href="/video34542905/mothers_fucked_in_front_of_their_daughters" 
            title="Mothers fucked in front of their daughters">Mothers fucked in front of their daughters
        </a>
    </p>
    <p class="metadata">
        <span class="bg">
            <span class="duration">2h 0 min</span>
            <a href="/profiles/vedius">Vedius</a>
            <span> - 7.8M Views</span>
            -
        </span>
    </p>
</div>
"""

regex_http = re.compile(r'(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\/\\\+&amp;%\$#_=]*)?')
regex_video_mp4 = re.compile(r'setVideoUrlHigh\(\'[\S^\)]+\'\)')
LIMIT = 24

CACHE_DURATION = 6 * 60 * 60 * 1000 # 6 hours

class XvSearchLogic(object):
    def __init__(self):
        self._keywords = { 'jav bj': 3, '91kk哥': 2, 'pron': 1}
        self._top3 = [ 'jav bj', '91kk哥', 'pron' ]
        self._mem_cache = {}

    def get_cache(self, key):
        if key in self._mem_cache:
            data = self._mem_cache[key]
            if data['valid_time'] < current_milli_time(): # un valid
                return False
            return data['document']
        return False

    def clean_cache(self):
        now = current_milli_time()
        for key, cache in self._mem_cache.items():
            if cache['valid_time'] < now:
                self._mem_cache.pop(key)

    def set_cache(self, key, document):
        self._mem_cache[key] = {
            'valid_time': current_milli_time() + CACHE_DURATION,
            'document': document
        }
        # TODO: drop the early cache
        self.clean_cache()

    def push_keyword(self, keyword):

        lower = keyword.lower()
        if lower in self._keywords:
            self._keywords[lower] = self._keywords[lower] + 1
        else:
            self._keywords[lower] = 1
        self.rank_keywords([lower, self._keywords[lower]])
        # TODO:drop the last entry if length 500

    def rank_keywords(self, entry):
        key = entry[0]
        num = entry[1]
        flag = False
        index = -1
        counter_list = []
        if key in self._top3:
            # sort the top3
            for top in self._top3:
                counter_list.append([self._keywords[top], top])
            counter_list = sorted(counter_list, key = itemgetter(0, 1), reverse = True)
            # reset the ranklist
            for i in range(3):
                self._top3[i] = counter_list[i][1]
        else:    
            # change a top3
            # should > the last one
            last_one = self._top3[2]
            last_one_count = self._keywords[last_one]
            if num >= last_one_count:
                self._top3[2] = key
            
    def get_top3_keywords(self):
        return self._top3

    def do_search(self, keywords = 'japan+blowjob', page = 0):
        # if page is 0 means ,it's an new search, we should sort the keywords
        if page == 0:
            self.push_keyword(keywords)
        cache_key = keywords + '-' + str(page)
        cache_document = self.get_cache(cache_key)
        if cache_document:
            return cache_document

        html = download(URL + keywords + '&p=' + str(page))
        total = 0
        max_page = 0
        self._root = etree.ElementTree(etree.HTML(html))
        self._content = etree.ElementTree(self._root.xpath('//div[@id="content"]')[0])
        self._data = []
        # self._title = self._root.xpath('//h2[@class="page-title"]')[0].text
        total = self._root.xpath('//h2[@class="page-title"]/span')[0].text.replace(',', '')
        r = str_search(total, re.compile(r'\d+'))
        if r:
            total = int(r)
            max_page = int(total/LIMIT)
        list_div = self._content.xpath('//div[@class="thumb-block "]')

        for div in list_div:
            data = {}
            div_tree = etree.ElementTree(div)
            data['href'] = VIDEO_PREFIX + div_tree.xpath('//div[@class="thumb"]/a/@href')[0]
            data['short_href'] = div_tree.xpath('//div[@class="thumb"]/a/@href')[0].strip('/').replace('/', '-')
            data['prev_image'] = div_tree.xpath('//div[@class="thumb"]/a/img/@data-src')[0]
            data['id'] = div_tree.xpath('//div[@class="thumb"]/a/img/@data-videoid')[0]
            data['title'] = div_tree.xpath('//p/a/@title')[0]
            spans = div_tree.xpath('//span[@class="bg"]/span/text()')
            data['duration'] = spans[0]
            if len(spans) > 1:
                data['views'] = spans[1]
            else:
                data['views'] = '-'
            # data['prev_video'] = div_tree.xpath('//div[@class="thumb"]/a/img/@data-src')[0]
            # https://images-llnw.xvideos-cdn.com/videos/thumbs169/8b/35/e3/8b35e3b9b528424a33a33d365bd9387b/8b35e3b9b528424a33a33d365bd9387b.26.jpg
            # https://images-llnw.xvideos-cdn.com/videos/videopreview/8b/35/e3/8b35e3b9b528424a33a33d365bd9387b_169.mp4
            self._data.append(data)

        cache_document = {'keywords': keywords, 'pagination': { 'current': int(page), 'max': max_page , 'total': total}, 'rows': self._data }
        self.set_cache(cache_key, cache_document)
        return cache_document

    def get_video(self, href):
        if not str_include(VIDEO_PREFIX, href):
            href = VIDEO_PREFIX + '/' + href
        video_html = download(href)
        video_script = etree.ElementTree(etree.HTML(video_html)).xpath('//div[@id="video-player-bg"]/script')[3].text
        r = str_search(video_script, regex_video_mp4)
        if r:
            return str_search(r, regex_http).strip()
        return False


