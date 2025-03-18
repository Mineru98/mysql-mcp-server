# -*- coding:utf-8 -*-
import json
from typing import List

from mcp.types import TextContent

from mysql_mcp_server.helper.db_conn_helper import DatabaseManager
from mysql_mcp_server.helper.logger_helper import logger
from mysql_mcp_server.helper.tool_decorator import tool


@tool()
def execute_show_tables(query: str) -> List[TextContent]:
    """
    데이터베이스에서 SHOW TABLE 쿼리를 실행하여 테이블 정보를 조회하는 함수입니다.
    이 함수는 MySQL 데이터베이스에 연결하여 사용자가 제공한 쿼리를 실행하고, 그 결과를 JSON 형식으로 반환합니다.
    주로 데이터베이스 내의 테이블 목록이나 테이블 상태를 확인할 때 사용됩니다.

    Args:
        query: 데이터베이스에 실행할 SHOW TABLE 관련 SQL 쿼리 문자열입니다.
    """
    conn = DatabaseManager.get_instance().get_connection()
    try:
        with conn.cursor() as cursor:
            logger.info(f"[execute_show_tables] query: {query}")
            if query.strip().upper().startswith("SHOW"):
                cursor.execute(query)
                result = cursor.fetchall()
                response_data = {"success": True, "data": result}
            else:
                response_data = {"success": False, "error": "Invalid query"}
    except Exception as e:
        response_data = {"success": False, "error": str(e)}

    result_text = json.dumps(response_data, ensure_ascii=False, indent=2)
    return [TextContent(type="text", text=result_text)]
