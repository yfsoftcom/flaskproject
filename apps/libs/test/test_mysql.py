# -*- coding: utf-8 -*-
import unittest
from libs.mysql import MysqlHelper

helper = MysqlHelper()

class TestMysqlHelper(unittest.TestCase):
    """Test MysqlHelper"""

    def setUp(self):
        helper.connect_db(db = "tzqiu")
        helper.execute('create table if not exists test(id int not null, val text not null)')
        helper.execute('delete from test')

    def tearDown(self):
        helper.close()

    def test_execute_and_find_one(self):
        """test_execute_and_find_one"""
        helper.execute('insert into test values(%d,\'%s\')', (1, 'abc'))
        row, e = helper.find_one('select * from test where id = %d', (1 ))
        self.assertTrue(e is None)
        self.assertEqual('abc', row[1])

    def test_find_all(self):
        """test_find_all"""
        helper.execute('insert into test values(%d,\'%s\')', (1, 'abc'))
        helper.execute('insert into test values(%d,\'%s\')', (2, 'bcd'))
        helper.execute('insert into test values(%d,\'%s\')', (3, 'ggg'))
        rows, e = helper.find_all('select * from test ')
        self.assertTrue(e is None)
        self.assertEqual(3, len(rows))
        self.assertEqual('ggg', rows[2][1])