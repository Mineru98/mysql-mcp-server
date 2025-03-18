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
    MySQL 데이터베이스에서 주어진 쿼리를 실행하여 데이터를 조회하는 함수입니다.
    주로 SELECT 쿼리를 실행하여 데이터를 가져오는 데 사용되며, 쿼리 결과 또는 실행 상태를 JSON 형식으로 반환합니다.

    Args:
        query: 실행할 MySQL 쿼리 문자열. SELECT로 시작하는 조회 쿼리를 포함할 수 있음.
    """
    conn = DatabaseManager.get_instance().get_connection()
    try:
        with conn.cursor() as cursor:
            logger.info(f"[execute_select_query] query: {query}")
            if query.strip().upper().startswith("SELECT"):
                cursor.execute(query)
                result = cursor.fetchall()
                for row in result:
                    for key, value in row.items():
                        if hasattr(value, "strftime"):
                            row[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                response_data = {"success": True, "data": result}
            else:
                response_data = {"success": False, "error": "Invalid query"}
    except Exception as e:
        response_data = {"success": False, "error": str(e)}

    result_text = json.dumps(response_data, ensure_ascii=False, indent=2)
    return [TextContent(type="text", text=result_text)]
