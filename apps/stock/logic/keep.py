import tushare as ts

from operator import itemgetter, attrgetter
from libs.kit import *
from libs.fpmc import *

import re,time, datetime

fpm = Fpmc()

# Fetch the keep stocks
data = fpm.call_func('common.find',{ 'table': 'stock_keep'}) 
print(data)

KEEP_STOCKS = [ [x['code'], int(x['hand']), float(x['cost'])] for x in data]
# [
#     ['sz002938', 1, 0.6],
#     ['sh600486', 3, 48.034],
#     ['sz300373', 8, 22.63],
#     ['sz000796', 17, 9.049],
#     ['sz300014', 5, 12.884],
#     ['sz002230', 1, 29.1],
#     ['sz002220', 21, 2.757],
# ]

def get_profit():
    rows = []
    total = { 'amount': 0.0, 'profit': 0.0 }
    origin = { 'amount': 0.0, 'rate': 0.0 }
    df = ts.get_realtime_quotes([ x[0] for x in KEEP_STOCKS])
    # print(df)
    for i in range(0, len(KEEP_STOCKS)):
        stock = KEEP_STOCKS[i]
        row = {}
        row['code'] = stock[0]
        # print(df)
        row['hand'] = stock[1]
        row['cost'] = stock[2]
        row['name'] = df.name[i]
        row['price'] = df.price[i]
        row['pre_close'] = df.pre_close[i]
        row['price_rate'] = round(( float(df.price[i]) - float(df.pre_close[i]) ) / float(df.pre_close[i]) * 100, 2)
        row['open'] = df.open[i]
        row['volume'] = int(int(df.volume[i]) / 100)

        if(float(stock[2]) > 0.1):
            # 总价
            row['amount'] = round(float(row['price']) * 100 * int(row['hand']), 2)
            # 收益， （现价-成本价） * 股数
            row['profit'] = round(( float(row['price']) - stock[2] ) * 100 * int(row['hand']), 2)
            # 收益率，（现价-成本价）/ 成本价
            row['rate'] = round(( float(row['price']) - stock[2] ) / stock[2] * 100, 2)
        else:
            row['amount'] = 0
            row['profit'] = 0
            row['rate'] = 0
        
        rows.append(row)
        total['amount'] = round(total['amount'] + row['amount'], 2)
        total['profit'] = round(total['profit'] + row['profit'], 2)
        
    origin['amount'] = round(total['amount'] - total['profit'], 2)
    origin['rate'] = round(total['profit'] / origin['amount'] * 100 , 2)

    rows = sorted(rows, key = itemgetter('amount'), reverse=True)
    return rows, total, origin


def sub_stock(code):
    data = fpm.call_func('common.create',{ 'table': 'stock_keep', 'row': { 'code': code }}) 
    return data

def buy_stock(code, hand, cost, fee = 5.0):
    data = fpm.call_func('common.create',{ 'table': 'stock_keep', 'row': { 'code': code }}) 
    return data
    
def get_trades():
    rows = []

    return rows