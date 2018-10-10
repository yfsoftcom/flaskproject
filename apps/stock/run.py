# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template, jsonify
from .logic.keep import *

stock = Blueprint('stock', __name__, template_folder='pages')


@stock.route('/')
def index():
    stocks, total, origin = get_profit()
    return render_template('stock/index.html', stocks = stocks, total = total, origin = origin)