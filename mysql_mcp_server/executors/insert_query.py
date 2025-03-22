# -*- coding:utf-8 -*-
import json
from typing import List

from mcp.types import TextContent

from mysql_mcp_server.helper.db_conn_helper import DatabaseManager
from mysql_mcp_server.helper.logger_helper import logger
from mysql_mcp_server.helper.tool_decorator import tool


@tool()
def execute_insert_query(query: str) -> List[TextContent]:
    """
    MySQL 데이터베이스에서 주어진 INSERT 쿼리를 실행하여 데이터를 삽입하는 함수입니다.
    INSERT INTO 쿼리를 실행하여 데이터베이스에 새 레코드를 추가하며, 실행 결과를 JSON 형식으로 반환합니다.

    Args:
        query: 실행할 MySQL INSERT 쿼리 문자열. 반드시 INSERT INTO로 시작해야 함.
    """
    conn = DatabaseManager.get_instance().get_connection()
    try:
        with conn.cursor() as cursor:
            logger.info(f"[execute_insert_query] query: {query}")
            if query.strip().upper().startswith("INSERT INTO"):
                cursor.execute(query)
                conn.commit()
                response_data = {"success": True, "affected_rows": cursor.rowcount}
            else:
                response_data = {
                    "success": False,
                    "error": "Only INSERT INTO queries are supported",
                }
    except Exception as e:
        response_data = {"success": False, "error": str(e)}

    result_text = json.dumps(response_data, ensure_ascii=False, indent=2)
    return [TextContent(type="text", text=result_text)]
