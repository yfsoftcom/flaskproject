# -*- coding: utf-8 -*-
import os, time, re, json
from operator import itemgetter, attrgetter
from libs.kit import *
from lxml import etree
import sqlite3

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

CREATE_TABLE_SEARCH_KEYWORDS_RECORD_CMD = '''create table if not exists search_keywords_record(
    search_content text primary key  not null,
    counter        int  not null);'''

CREATE_TABLE_SEARCH_CACHE_CMD = '''create table if not exists search_cache(
    cache_key text primary key  not null,
    cache_document text not null,
    valid_time int not null);'''


CREATE_TABLE_VIDEOS_CMD = '''create table if not exists x_videos(
    id int primary key  not null,
    src text  not null,
    title text not null,
    star int  not null);'''



class XvSearchLogic(object):
    def __init__(self):
        self._conn = sqlite3.connect('test.db', check_same_thread = False)
        self.init_db()

    def __del__(self):
        self._conn.close()

    def init_db(self):
        cursor = self._conn.cursor()
        # create table
        cursor.execute(CREATE_TABLE_SEARCH_KEYWORDS_RECORD_CMD)
        cursor.execute(CREATE_TABLE_SEARCH_CACHE_CMD)
        cursor.execute(CREATE_TABLE_VIDEOS_CMD)
        self._conn.commit()

        cursor.execute('select count(*) from search_keywords_record')
        num = cursor.fetchone()[0]
        if num == 0:
            cursor.execute("insert into search_keywords_record values (?, ?)", ('jav bj', 3))
            cursor.execute("insert into search_keywords_record values (?, ?)", ('91kk哥', 2))
            cursor.execute("insert into search_keywords_record values (?, ?)", ('pron', 1))

        self._conn.commit()
        cursor.close()

    def get_cache(self, key):
        cursor = self._conn.cursor()
        cursor.execute("select cache_document from search_cache where cache_key=?", (key,))
        cache = cursor.fetchone()
        cursor.close()
        if cache is None:
            return False
        return json.loads(cache[0])

        # if key in self._mem_cache:
        #     data = self._mem_cache[key]
        #     if data['valid_time'] < current_milli_time(): # un valid
        #         return False
        #     return data['document']
        # return False

    def clean_cache(self):
        now = current_milli_time()
        
        cursor = self._conn.cursor()
        cursor.execute("delete from search_cache where valid_time < ?", (now,))

        self._conn.commit()
        cursor.close()

    def set_cache(self, key, document):
        cursor = self._conn.cursor()
        cursor.execute("insert into search_cache values (?, ?, ?)", (key, json.dumps(document), current_milli_time() + CACHE_DURATION))

        self._conn.commit()
        cursor.close()

        self.clean_cache()

    def push_keyword(self, keyword):

        lower = keyword.lower()
        cursor = self._conn.cursor()
        
        cursor.execute('select count(*) as num from search_keywords_record where search_content=\'%s\'' % lower )
        
        # 获得查询结果集:
        num = cursor.fetchone()[0]
        if num > 0:
            cursor.execute("update search_keywords_record set counter = counter + 1 where search_content='%s'" % lower )
        else:
            cursor.execute("insert into search_keywords_record values (?, ?)", (lower, 1))
        self._conn.commit()
        cursor.close()
        """
        ### dep 使用sqlite3替换
        #### 
        if lower in self._keywords:
            self._keywords[lower] = self._keywords[lower] + 1
        else:
            self._keywords[lower] = 1
        self.rank_keywords([lower, self._keywords[lower]])
        # TODO:drop the last entry if length 500
        """

    """
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
    """

    def get_top3_keywords(self):
        cursor = self._conn.cursor()
        cursor.execute('select search_content from search_keywords_record order by counter desc limit 3 offset 0')
        top3 = []
        for row in cursor:
            top3.append(row[0])
        cursor.close()
        return top3

    def get_hot_rank(self):
        cursor = self._conn.cursor()
        cursor.execute('select * from x_videos order by star desc limit 10 offset 0')
        hot_rank = []
        for row in cursor:
            hot_rank.append({ 'id': row[0], 'src': row[1], 'title': row[2], 'star': row[3] })
        cursor.close()
        return hot_rank

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

    def get_video(self, vid, href):
        vid = int(vid)
        cursor = self._conn.cursor()
        cursor.execute("select * from x_videos where id=?", (vid,))
        row = cursor.fetchone()
        cursor.close()
        if row is not None:
            return { 'id': row[0], 'src': row[1], 'title': row[2], 'star': row[3] }
        
        if not str_include(VIDEO_PREFIX, href):
            href = VIDEO_PREFIX + '/' + href
        video_html = download(href)
        root = etree.ElementTree(etree.HTML(video_html))
        video_title = root.xpath('//title')[0].text
        video_script = root.xpath('//div[@id="video-player-bg"]/script')[3].text
        
        r = str_search(video_script, regex_video_mp4)
        if r:
            src = str_search(r, regex_http).strip()
            cursor = self._conn.cursor()
            cursor.execute("insert into x_videos values (?, ?, ?, ?)", (vid, src, video_title, 0) )
            self._conn.commit()
            cursor.close()
            return { 'id': vid, 'src': src, 'title': video_title, 'star': 0 }
        return False

    def star(self, vid):
        cursor = self._conn.cursor()

        cursor.execute("update x_videos set star = star + 1 where id=?", (int(vid), ) )
        
        self._conn.commit()
        cursor.close()
        return {'errno': 0}

