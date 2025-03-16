# -*- coding:utf-8 -*-
import pymysql


class DatabaseManager:
    _instance = None
    conn = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DatabaseManager()
        return cls._instance

    def connect(self, config):
        if self.conn is None:
            self.conn = pymysql.connect(**config)
        return self.conn

    def get_connection(self):
        return self.conn
