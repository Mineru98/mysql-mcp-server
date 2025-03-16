# -*- coding:utf-8 -*-
import asyncio
import os
import sys

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fire
import pymysql.cursors
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server

from mysql_mcp_server.excutors import TOOLS_DEFINITION
from mysql_mcp_server.handlers import handle_call_tool, handle_list_tools
from mysql_mcp_server.helper.db_conn_helper import DatabaseManager
from mysql_mcp_server.helper.logger_helper import logger

load_dotenv()


class MySQLMCPServer:
    def __init__(
        self,
        mcp_port: int = int(os.getenv("MCP_PORT", 8081)),
        mysql_host: str = os.getenv("MYSQL_HOST", "localhost"),
        mysql_port: int = int(os.getenv("MYSQL_PORT", 3306)),
        mysql_user: str = os.getenv("MYSQL_USER", "root"),
        mysql_password: str = os.getenv("MYSQL_PASSWORD", "mcpTest1234!!!"),
        mysql_database: str = os.getenv("MYSQL_DATABASE", "mcp_test"),
        stdio: bool = False,
    ):
        self.port = mcp_port
        self.mysql_config = {
            "host": mysql_host,
            "port": mysql_port,
            "user": mysql_user,
            "password": mysql_password,
            "database": mysql_database,
            "cursorclass": pymysql.cursors.DictCursor,
        }
        self.stdio = stdio
        self.__setup_server()

    def __setup_server(self):
        try:
            self.__connect_to_mysql()
        except Exception as e:
            logger.error(f"MySQL 연결 오류: {e}")
            sys.exit(1)

        if self.stdio:
            self.server = Server("MySQL MCP 서버")
            self.server.list_tools()(handle_list_tools)
            self.server.call_tool()(handle_call_tool)
        else:
            logger.info(f"서버가 포트 {self.port}에서 시작됩니다.")
            self.mcp = FastMCP(name="MySQL MCP 서버", debug=True, port=self.port)
            self.__setup_tools()

    def __connect_to_mysql(self):
        db_manager = DatabaseManager.get_instance()
        db_manager.connect(self.mysql_config)
        self.conn = db_manager.get_connection()

    def __setup_tools(self):
        for tool_schema in TOOLS_DEFINITION:
            self.mcp.tool()(tool_schema)

    async def __stdio_main(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, write_stream, self.server.create_initialization_options(), raise_exceptions=True
            )

    def run(self):
        if self.stdio:
            logger.info("Starting MCP...")
            asyncio.run(self.__stdio_main())
        else:
            logger.info("Starting MCP server...")
            self.mcp.run(transport="sse")


def main():
    fire.Fire(MySQLMCPServer)


if __name__ == "__main__":
    main()
