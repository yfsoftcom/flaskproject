# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, jsonify
from libs.kit import *
from .logic.search import XvSearchLogic

xv = Blueprint('xv', __name__, template_folder='pages')

logic = XvSearchLogic()

@xv.route('/')
def index():
    return render_template('xv/index.html')

# http://localhost:5000/api/search/p/1/japan+blowjob

@xv.route('/api/search/p/<page>/<keyword>')
def api_search_by_page(page, keyword):
    data = logic.do_search(keyword, int(page))
    return jsonify(data)

# http://localhost:5000/api/top3
@xv.route('/api/top3')
def api_get_top3_search_keywords():
    data = logic.get_top3_keywords()
    return jsonify(data)

# http://localhost:5000/api/video/34542905/video34542905-mothers_fucked_in_front_of_their_daughters
@xv.route('/api/video/<vid>/<url>')
def api_get_video(vid, url):
    url = url.replace('-', '/')
    data = logic.get_video(vid, url)
    return jsonify(data)

@xv.route('/api/star/<vid>')
def api_star_video(vid):
    data = logic.star(vid)
    return jsonify(data)

@xv.route('/changelog')
def changelog():
    return render_template('xv/changelog.html')


@xv.route('/hot')
def hot():
    return render_template('xv/hot.html')

@xv.route('/api/hot_rank')
def api_get_hot_rank():
    data = logic.get_hot_rank()
    return jsonify(data)