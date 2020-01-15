# -*- coding: utf-8 -*-
from flask import Flask
from libs.kit import *
from xv_search.run import xv
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.FileHandler',
        'filename': 'app.log',
        'formatter': 'default'
    }},
    'root': {
        'level': 'ERROR',
        'handlers': ['file']
    }
})
app = Flask(__name__)

app.register_blueprint(xv, url_prefix='/xv')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True) 