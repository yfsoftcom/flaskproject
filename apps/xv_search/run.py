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
    data = logic.do_search(keyword, page)
    return jsonify(data)

# http://localhost:5000/api/video/video34542905-mothers_fucked_in_front_of_their_daughters
@xv.route('/api/video/<url>')
def api_get_video(url):
    url = url.replace('-', '/')
    data = logic.get_video(url)
    return jsonify({'origin_mp4': data})
