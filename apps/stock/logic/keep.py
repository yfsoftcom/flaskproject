import tushare as ts

from libs.kit import *

import re,time, datetime

KEEP_STOCKS = [
    ['sz002938', 2, 9.121],
    ['sh600486', 3, 48.034],
    ['sz300373', 6, 24.34],
    ['sz000796', 13, 9.894],
    ['sz300014', 3, 13.623],
    ['sz002230', 1, 29.1],
]

def get_profit():
    rows = []
    total = { 'amount': 0.0, 'profit': 0.0 }
    origin = { 'amount': 0.0, 'rate': 0.0 }
    for stock in KEEP_STOCKS:
        row = {}
        row['code'] = stock[0]
        df = ts.get_realtime_quotes(stock[0])
        row['hand'] = stock[1]
        row['cost'] = stock[2]
        row['name'] = df.name[0]
        row['price'] = df.price[0]
        # 总价
        row['amount'] = round(float(row['price']) * 100 * int(row['hand']), 2)
        # 收益， （现价-成本价） * 股数
        row['profit'] = round(( float(row['price']) - stock[2] ) * 100 * int(row['hand']), 2)
        # 收益率，（现价-成本价）/ 成本价
        row['rate'] = round(( float(row['price']) - stock[2] ) / stock[2] * 100, 2)
        rows.append(row)
        total['amount'] = round(total['amount'] + row['amount'], 2)
        total['profit'] = round(total['profit'] + row['profit'], 2)
        
    origin['amount'] = round(total['amount'] - total['profit'], 2)
    origin['rate'] = round(total['profit'] / origin['amount'] * 100 , 2)
    return rows, total, origin