# -*- coding:utf-8 -*-
import json
from typing import List

from mcp.types import TextContent

from mysql_mcp_server.helper.db_conn_helper import DatabaseManager
from mysql_mcp_server.helper.logger_helper import logger
from mysql_mcp_server.helper.tool_decorator import tool


@tool()
def execute_explain(query: str) -> List[TextContent]:
    """
    MySQL 데이터베이스에서 EXPLAIN 키워드를 사용해 쿼리의 실행 계획을 분석하고 결과를 반환하는 함수.
    이 함수는 주어진 쿼리가 데이터베이스에서 어떻게 실행되는지 이해할 수 있도록 실행 계획 정보를 제공하며,
    쿼리 최적화 및 성능 분석에 활용된다. EXPLAIN이 포함되지 않은 쿼리의 경우 오류 메시지를 반환한다.

    Args:
        query: 실행 계획을 확인하고자 하는 MySQL 쿼리 문자열. 반드시 EXPLAIN 키워드로 시작해야 함.
    """
    conn = DatabaseManager.get_instance().get_connection()
    try:
        with conn.cursor() as cursor:
            logger.info(f"[execute_explain] query: {query}")
            if query.strip().upper().startswith("EXPLAIN"):
                cursor.execute(query)
                result = cursor.fetchall()
                response_data = {"success": True, "data": result}
            else:
                response_data = {"success": False, "error": "Invalid query"}
    except Exception as e:
        response_data = {"success": False, "error": str(e)}

    result_text = json.dumps(response_data, ensure_ascii=False, indent=2)
    return [TextContent(type="text", text=result_text)]
