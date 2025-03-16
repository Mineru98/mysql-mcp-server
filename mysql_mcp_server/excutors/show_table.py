# -*- coding:utf-8 -*-
import json
from typing import List

from mcp.types import TextContent

from mysql_mcp_server.helper.db_conn_helper import DatabaseManager
from mysql_mcp_server.helper.logger_helper import logger
from mysql_mcp_server.helper.tool_decorator import tool


@tool()
def execute_show_table(query: str) -> List[TextContent]:
    """
    Run a MySQL show table query

    Args:
        query: MySQL 테이블 조회 문자열

    Returns:
        MySQL 테이블 조회 결과
    """
    conn = DatabaseManager.get_instance().get_connection()
    try:
        with conn.cursor() as cursor:
            logger.info(f"[execute_show_table] query: {query}")
            cursor.execute(query)
        result = cursor.fetchall()
        response_data = {"success": True, "data": result}
    except Exception as e:
        response_data = {"success": False, "error": str(e)}

    result_text = json.dumps(response_data, ensure_ascii=False, indent=2)
    return [TextContent(type="text", text=result_text)]
