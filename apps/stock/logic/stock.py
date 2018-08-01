import tushare as ts
#将所有的股票名称和股票代码、行业、地区写入到名为allstock的表中，这个文件只需要执行一次
from libs.mysql import MysqlHelper
from libs.kit import *

import re,time, datetime

helper = MysqlHelper()

SQL_TABLE_ALL_STOCK = """CREATE TABLE IF NOT EXISTS `allstock` (
  `id` int(11) NOT NULL,
  `delflag` tinyint(4) NOT NULL DEFAULT '0',
  `createAt` bigint(20) DEFAULT NULL,
  `updateAt` bigint(20) DEFAULT NULL,
  `code` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `industry` varchar(100) NOT NULL,
  `area` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

SQL_TABLE_STOCK_HIST = """create table IF NOT EXISTS stock_history (
	code varchar(32), 
	date varchar(32),
	open varchar(32),
	close varchar(32),
	high varchar(32),
	low varchar(32),
	volume varchar(32),
	p_change varchar(32)
	)ENGINE=InnoDB DEFAULT CHARSET=utf8;"""


SQL_INSERT_STOCK = "insert into allstock (code,name,industry,area,createAt,updateAt) values ('%s','%s','%s','%s',%d,%d)"
SQL_INSERT_STOCK_HIST = "insert into stock_history (code,date,open,close,high,low,volume,p_change) values ('%s','%s','%s','%s','%s','%s','%s','%s')"

SQL_DELETE_STOCK_HIST_BY_CODE_AND_DATE = "delete from stock_history where code = '%s' and date = '%s'"

def create_table():
	# connect the db
	helper.connect_db(db = "stock", host = 'localhost')
	helper.execute(SQL_TABLE_ALL_STOCK)
	helper.execute(SQL_TABLE_STOCK_HIST)
	helper.close()
	return True, None

def save_all_stocks():

	# fetch all stock baisc info from tushare
	stock_info = ts.get_stock_basics()

	codes = stock_info.index
	names = stock_info.name
	industrys = stock_info.industry
	areas = stock_info.area

	# save to db
	total = len(stock_info)
	now = current_milli_time()
	helper.connect_db(db = "stock", host = 'localhost')
	for i in range(0, total):
		helper.execute(
			SQL_INSERT_STOCK, 
			(
				codes[i],
				names[i],
				industrys[i],
				areas[i],
				now,
				now 
			))
	
	helper.close()
	return total


def fetch_stock_hist(stock_code = [], starttime = '2016-01-01', endtime = '2018-01-01'):
	if len(stock_code) == 0:
		# fetch all stock baisc info from tushare
		stock_info = ts.get_stock_basics()
		codes = stock_info.index
	else:
		codes = stock_code 
	# connect db
	helper.connect_db(db = "stock", host = 'localhost')
	
	total = len(codes)

	counter = 0
	
	for x in range(0, total):
		# fetch the stock's history
		df = ts.get_k_data(code = codes[x], start = starttime, end = endtime)
		rows = len(df)
		print(df)
		counter += rows
		if df is None:
			# the stock maybe paused, so we cannt get anything
			continue
		try:
			for i in range(0, rows):
				# format the day time
				times = time.strptime(df.index[i], '%Y-%m-%d')
				time_new = time.strftime('%Y%m%d', times)
				# delete the day history if exists, in case of the history repeated
				helper.execute(
					SQL_DELETE_STOCK_HIST_BY_CODE_AND_DATE,
					(
						codes[x], 
						time_new
					)
				)
				# insert the day history
				helper.execute(
					SQL_INSERT_STOCK_HIST, 
						(
							codes[x], 
							time_new,
							df.open[i],
							df.close[i],
							df.high[i],
							df.low[i],
							df.volume[i],
							df.p_change[i]
						))
				
		except Exception as e:
			pass
 
	helper.close()
	
	return total, counter

# learn from the history
def learn_stock(stock_code = [], start = '2016-01-01', end = '2018-12-31'):
	pass

def get_stock_big_trade(stock_code = [], day = None):
	if day is None:
		day = ''
	df = ts.get_sina_dd('000796', date='2018-07-31', vol=500) #默认400手
	return df