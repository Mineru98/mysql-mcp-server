# -*- coding:utf-8 -*-
import json
from typing import List

from mcp.types import TextContent

from mysql_mcp_server.helper.db_conn_helper import DatabaseManager
from mysql_mcp_server.helper.logger_helper import logger
from mysql_mcp_server.helper.tool_decorator import tool


@tool()
def execute_select_query(query: str) -> List[TextContent]:
    """
    Run a read-only MySQL query

    Args:
        query: MySQL 쿼리 문자열

    Returns:
        MySQL 쿼리 결과
    """
    conn = DatabaseManager.get_instance().get_connection()
    try:
        with conn.cursor() as cursor:
            logger.info(f"[execute_select_query] query: {query}")
            cursor.execute(query)
            if (
                query.strip().upper().startswith("SELECT")
                or query.strip().upper().startswith("DESCRIBE")
                or query.strip().upper().startswith("DESC")
                or query.strip().upper().startswith("SHOW")
                or query.strip().upper().startswith("EXPLAIN")
            ):
                result = cursor.fetchall()
                response_data = {"success": True, "data": result}
            else:
                conn.commit()
                response_data = {"success": True, "affected_rows": cursor.rowcount}
    except Exception as e:
        response_data = {"success": False, "error": str(e)}

    result_text = json.dumps(response_data, ensure_ascii=False, indent=2)
    return [TextContent(type="text", text=result_text)]
