# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, jsonify
from libs.kit import *
from .logic.search import XvSearchLogic
from .logic.rss import XvRssLogic

from .logic.user import UserLogic

xv = Blueprint('xv', __name__, template_folder='pages')

logic = XvSearchLogic()
user = UserLogic()
rss = XvRssLogic()

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
@xv.route('/api/video/<vid>/<href>')
def api_get_video(vid, href):
    data = logic.get_video(vid, href)
    return jsonify(data)

@xv.route('/api/star/<vid>')
def api_star_video(vid):
    data = logic.star(vid)
    return jsonify(data)

@xv.route('/api/user/register', methods=['POST'])
def api_user_register():
    data = json.loads(request.get_data(as_text=True))
    data = user.register(data)
    return jsonify(data)

@xv.route('/api/user/login', methods=['POST'])
def api_user_login():
    data = json.loads(request.get_data(as_text=True))
    data = user.login(data['username'], data['password'])
    return jsonify(data)

@xv.route('/api/favorite/add', methods=['POST'])
def api_favorite_add():
    data = json.loads(request.get_data(as_text=True))
    username = data['username']
    del data['username']
    data = user.favorite(username, data['vid'], data)
    return jsonify(data)

@xv.route('/api/favorite/del', methods=['POST'])
def api_favorite_del():
    data = json.loads(request.get_data(as_text=True))
    data = user.del_favorite(data['username'], data['vid'])
    return jsonify(data)

@xv.route('/api/favorite/list/<username>')
def api_favorite_list(username):
    data = user.list_favorite(username)
    return jsonify(data)

@xv.route('/changelog')
def changelog():
    return render_template('xv/changelog.html')


@xv.route('/hot')
def hot():
    return render_template('xv/hot.html')

@xv.route('/latest')
def latest():
    return render_template('xv/latest.html')

@xv.route('/api/hot_rank')
def api_get_hot_rank():
    data = logic.get_hot_rank()
    return jsonify(data)

@xv.route('/api/rss')
def api_get_rss():
    data = rss.parse()
    return jsonify(data)