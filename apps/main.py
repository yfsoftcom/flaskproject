# -*- coding: utf-8 -*-
from flask import Flask
from libs.kit import *
from xv_search.run import xv
from worldcup2018.run import worldcup

app = Flask(__name__)

app.register_blueprint(xv, url_prefix='/xv')
app.register_blueprint(worldcup, url_prefix='/worldcup')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True) 