# -*- coding: utf-8 -*-
"""
its for mysql helper
"""
import pymysql

class MysqlHelper(object):

    def __init__(self):
        self._auto_commit = True
        self._is_cursor_open = False
        self._cursor = None
        self._is_closed = False

    def __del__(self):
        if self._is_closed:
            return
        try:
            self.close()
        except:
            pass
        finally:
            pass

    def connect_db(self, host = '127.0.0.1', port = 3306 , user = 'root', passowrd = 'root', db = 'test'):
        self._conn = pymysql.connect( host, user, passowrd, db )

    def open_cursor(self):
        if not self._is_cursor_open:
            self._is_cursor_open = True
            self._cursor = self._conn.cursor()
        return self._cursor   

    def close_cursor(self):
        if self._is_cursor_open:
            if self._cursor is not None:
                self._cursor.close()
            self._cursor = None            
            self._is_cursor_open = False
    
    def begin_trans(self):
        self.commit()
        self._auto_commit = False        

    def execute(self, sql, options = ()):
        try:
            cursor = self.open_cursor()
            cursor.execute(sql % options)
            if self._auto_commit:
                self.commit()
        except Exception as e:
            raise e
            
    def convert_fields(self, row, fields = None):
        if row is None:
            return None
        if fields is None:
            return row

        entity = {}
        for i, field in enumerate(fields):
            entity[field] = row[i]
        return entity

    def find_all(self, sql, options = (), fields = None):
        try:
            cursor = self.open_cursor()
            cursor.execute(sql % options)
            results = cursor.fetchall()
            rows = [ self.convert_fields(row, fields) for row in results ]
            if self._auto_commit:
                self.commit()
            return rows, None
        except Exception as e:
            print(e)
            return None, e

    def find_one(self, sql, options = (), fields = None):
        try:
            cursor = self.open_cursor()
            cursor.execute(sql % options)
            row = cursor.fetchone()
            row = self.convert_fields(row, fields)
            if self._auto_commit:
                self.commit()
            return row, None
        except Exception as e:
            print(e)
            return None, e
    
    def commit(self):
        try:
            self._conn.commit()
            self._auto_commit = False
            self.close_cursor()
        finally:
            pass

    def rollback(self):
        try:
            self._conn.rollback()
            self._auto_commit = False
            self.close_cursor()
        finally:
            pass

    def close(self):
        try:
            self.commit()
            self._conn.close()
        finally:
            self._is_closed = True