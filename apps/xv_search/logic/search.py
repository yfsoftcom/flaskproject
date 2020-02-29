# -*- coding: utf-8 -*-
import os, time, re, json
from operator import itemgetter, attrgetter
from flask import current_app
from libs.kit import *
from lxml import etree
from .env import URL, VIDEO_PREFIX, VIDEO_FRAME, redisHelper

"""
2020-01-14 update
<div id="video_19129995" data-id="19129995" class="thumb-block ">
   <div class="thumb-inside">
      <div class="thumb">
         <a href="/video19129995/due_west_our_sex_journey_2012_">
            <img src="https://static-l3.xvideos-cdn.com/img/lightbox/lightbox-blank.gif" data-src="https://img-hw.xvideos-cdn.com/videos/thumbs169ll/7e/2b/9d/7e2b9d8c190fd8701c1e3271fca2851f/7e2b9d8c190fd8701c1e3271fca2851f.9.jpg" data-idcdn="2" data-videoid="19129995" id="pic_19129995" />
         </a>
      </div>
      <span class="video-hd-mark">720p</span>
   </div>
   <div class="thumb-under">
      <p class="title">
         <a href="/video19129995/due_west_our_sex_journey_2012_" title="Due West Our Sex Journey (2012)">Due West Our Sex Journey (2012)</a>
      </p>
      <p class="metadata">
         <span class="bg">
            <span class="duration">18 min</span>
            <a href="/profiles/maybelle_camryn">
               <span class="name">Maybelle Camryn</span>
            </a>
            <span>
               <span class="sprfluous">-</span>
               2.1M
               <span class="sprfluous">Views</span>
            </span>
            <span class="sprfluous">-</span>
         </span>
      </p>
   </div>
   <script>xv.thumbs.prepareVideo(19129995);</script>
</div>
"""

"""
html5player.setVideoUrlLow('https://video-hw.xvideos-cdn.com/videos/3gp/c/3/2/xvideos.com_c321e01b8252276499cd5be7f2a3bf4a.mp4?e=1578971139&ri=1024&rs=85&h=5ce157151ad8474f120a942bd9944a9c');
html5player.setVideoUrlHigh('https://video-hw.xvideos-cdn.com/videos/mp4/c/3/2/xvideos.com_c321e01b8252276499cd5be7f2a3bf4a.mp4?e=1578971139&ri=1024&rs=85&h=2e6092ee702317d01929fca55780269e');
html5player.setVideoHLS('https://hls-hw.xvideos-cdn.com/videos/hls/c3/21/e0/c321e01b8252276499cd5be7f2a3bf4a/hls.m3u8?e=1578971139&l=0&h=a5f1e53ff4de8f29dea2cdfb1d13fcb5');
"""

regex_http = re.compile(r'(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\/\\\+&amp;%\$#_=]*)?')
regex_video_mp4 = re.compile(r'setVideoUrlLow\(\'[\S^\)]+\'\)')
regex_video_hd = re.compile(r'setVideoUrlHigh\(\'[\S^\)]+\'\)')
regex_video_title = re.compile(r'setVideoTitle\(\'[ \S^\)]+\'\)')
LIMIT = 24

CACHE_DURATION = 6 * 60 * 60  # 6 hours

ONE_HOUR = 60 * 60  # 1h

class XvSearchLogic(object):
    def __init__(self):
        self._r = redisHelper

    def __del__(self):
        self._r.close()

    def get_cache(self, key):
        cache = self._r.get('search:' + key)
        if cache != None:
            return json.loads(cache)

    def clean_cache(self):
        pass

    def set_cache(self, key, document):
        self._r.setex('search:' + key, document, CACHE_DURATION)

    def push_keyword(self, keyword):
        lower = keyword.lower()
        self._r.get_instance().zincrby('search_keywords_record', -1, lower)

    def get_top3_keywords(self):
        rows = self._r.get_instance().zrange('search_keywords_record', start=0, end=3, withscores=False)
        return [ str(x, 'utf8') for x in rows ]

    def get_hot_rank(self):
        rows = self._r.get_instance().zrange('video_star', start=0, end=10, withscores=False)
        return rows

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
            href = VIDEO_PREFIX + div_tree.xpath('//div[@class="thumb"]/a/@href')[0]
            data['href'] = href.split('/')[-1]
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
            
            current_app.logger.info(data['id'])
            current_app.logger.info(data['href'])
            self._data.append(data)

        cache_document = {'keywords': keywords, 'pagination': { 'current': int(page), 'max': max_page , 'total': total}, 'rows': self._data }
        self.set_cache(cache_key, json.dumps(cache_document))
        return cache_document

    def get_video(self, vid, href):
        vid = int(vid)
        now = current_milli_time()
        is_include = False
        row = self._r.get_instance().hget("videos", str(vid))
        if row is not None:
            is_include = True
            row = json.loads(row)
            if int(row['valid_time']) > now:
                return row
        current_app.logger.info(VIDEO_PREFIX + '/video' + str(vid) + '/' + href)
        video_html = download(VIDEO_PREFIX + '/video' + str(vid) + '/' + href)
        # print(video_html)
        current_app.logger.info(video_html)
        root = etree.ElementTree(etree.HTML(video_html))
        # video_title = root.xpath('//title')[0].text
        video_script = root.xpath('//body//script[contains(text(), "setVideoUrlLow")]')[0].text
        video_cover = root.xpath('//meta[@property="og:image"]/@content')[0]
        video_title = str_search(video_script, regex_video_title)
        video_title = str_search(video_title, re.compile(r'\'[ \S^\)]+\'')).replace('\'', '')
        r = str_search(video_script, regex_video_mp4)
        hd_r = str_search(video_script, regex_video_hd)
        if r and hd_r:
            src = str_search(r, regex_http).strip()
            hd = str_search(hd_r, regex_http).strip()
            one = { 'id': vid, 'hd': hd, 'cover': video_cover,'src': src, 'href': href, 'title': video_title, 'star': 0, 'valid_time': now + ONE_HOUR }
            self._r.get_instance().hset("videos", str(vid), json.dumps(one))
            return one
        return False

    def star(self, vid):
        row = json.loads(self._r.get_instance().hget("videos", str(vid)))
        row['star'] = row['star'] + 1
        self._r.get_instance().hset("videos", str(vid), json.dumps(row))
        self._r.get_instance().zincrby('video_star', -1, row['title'])
        return {'errno': 0}

