# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, jsonify
from .logic.keep import *

stock = Blueprint('stock', __name__, template_folder='pages')


@stock.route('/')
def index():
    return render_template('stock/index.html')

@stock.route('/api/keep')
def api_get_keep():
    stocks, total, origin = get_profit()
    return jsonify({'stocks': stocks, 'total': total, 'origin': origin})

@stock.route('/api/sub/<code>')
def api_sub_stock(code):
    data = sub_stock(code)
    return jsonify(data)
    
@stock.route('/trade')
def trade():
    return render_template('stock/trade.html')
