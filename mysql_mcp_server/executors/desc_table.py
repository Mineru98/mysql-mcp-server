# -*- coding:utf-8 -*-
import json
from typing import List

from mcp.types import TextContent

from mysql_mcp_server.helper.db_conn_helper import DatabaseManager
from mysql_mcp_server.helper.logger_helper import logger
from mysql_mcp_server.helper.tool_decorator import tool


@tool()
def execute_desc_table(query: str) -> List[TextContent]:
    """
    데이터베이스 테이블의 구조를 조회하거나, 주어진 쿼리를 실행하여 테이블의 메타데이터 정보를 반환하는 함수입니다.
    주로 'DESC'로 시작하는 쿼리를 처리하며, 테이블의 컬럼 정보 등을 확인할 때 사용됩니다.
    쿼리 실행 결과를 JSON 형식의 문자열로 변환하여 반환합니다.

    Args:
        query: 데이터베이스에 실행할 SQL 쿼리 문자열. 'DESC'로 시작하는 경우 테이블 구조를 조회하며, 그 외의 경우 쿼리 실행 결과를 처리합니다.
    """
    conn = DatabaseManager.get_instance().get_connection()
    try:
        with conn.cursor() as cursor:
            logger.info(f"[execute_desc_table] query: {query}")
            cursor.execute(query)
            if query.strip().upper().startswith("DESC"):
                result = cursor.fetchall()
                response_data = {"success": True, "data": result}
            else:
                conn.commit()
                response_data = {"success": True, "affected_rows": cursor.rowcount}
    except Exception as e:
        response_data = {"success": False, "error": str(e)}

    result_text = json.dumps(response_data, ensure_ascii=False, indent=2)
    return [TextContent(type="text", text=result_text)]
