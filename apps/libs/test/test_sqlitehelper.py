# -*- coding: utf-8 -*-
import unittest
from libs.sqlite import Sqlite3Helper
from lxml import etree

helper = Sqlite3Helper()

class TestSqliteHelper(unittest.TestCase):
    """Test Sqlite3Helper"""

    def setUp(self):
        helper.connect_db('data.db')
        helper.execute('create table if not exists test(id int not null, val text not null)')
        helper.execute('delete from test')

    def tearDown(self):
        helper.close()

    def test_execute_and_find_one(self):
        """test_execute_and_find_one"""
        helper.execute('insert into test values(?,?)', (1, 'abc',))
        row, e = helper.find_one('select * from test where id = ?', (1, ))
        self.assertTrue(e is None)
        self.assertEqual('abc', row[1])

    def test_find_all(self):
        """test_find_all"""
        helper.execute('insert into test values(?,?)', (1, 'abc',))
        helper.execute('insert into test values(?,?)', (2, 'bcd',))
        helper.execute('insert into test values(?,?)', (3, 'ggg',))
        rows, e = helper.find_all('select * from test ')
        self.assertTrue(e is None)
        self.assertEqual(3, len(rows))
        self.assertEqual('ggg', rows[2][1])