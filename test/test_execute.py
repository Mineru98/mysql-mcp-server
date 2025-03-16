# -*- coding:utf-8 -*-
import os
import sys
import unittest

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql.cursors

from mysql_mcp_server.executors.select_query import execute_select_query
from mysql_mcp_server.helper.db_conn_helper import DatabaseManager


class TestExecute(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager.get_instance()
        mysql_host: str = os.getenv("MYSQL_HOST", "localhost")
        mysql_port: int = int(os.getenv("MYSQL_PORT", 3306))
        mysql_user: str = os.getenv("MYSQL_USER", "root")
        mysql_password: str = os.getenv("MYSQL_PASSWORD", "mcpTest1234!!!")
        mysql_database: str = os.getenv("MYSQL_DATABASE", "mcp_test")
        self.mysql_config = {
            "host": mysql_host,
            "port": mysql_port,
            "user": mysql_user,
            "password": mysql_password,
            "database": mysql_database,
            "cursorclass": pymysql.cursors.DictCursor,
        }
        self.db.connect(self.mysql_config)

    def test_select_query(self):
        pass
        # result = execute_select_query("SELECT * FROM users")


if __name__ == "__main__":
    unittest.main()
