# -*- coding: utf-8 -*-
from flask import Flask
from libs.kit import *
from xv_search.run import xv
# from worldcup2018.run import worldcup
# from stock.run import stock

app = Flask(__name__)

app.register_blueprint(xv, url_prefix='/xv')
# app.register_blueprint(worldcup, url_prefix='/worldcup')
# app.register_blueprint(stock, url_prefix='/stock')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True) 