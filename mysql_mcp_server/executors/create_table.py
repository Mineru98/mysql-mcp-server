# -*- coding:utf-8 -*-
import json
from typing import List

from mcp.types import TextContent

from mysql_mcp_server.helper.db_conn_helper import DatabaseManager
from mysql_mcp_server.helper.logger_helper import logger
from mysql_mcp_server.helper.tool_decorator import tool


@tool()
def execute_create_table(query: str) -> List[TextContent]:
    """
    MySQL 데이터베이스에서 새로운 테이블을 생성하는 기능을 제공합니다.
    이 함수는 주어진 MySQL 쿼리문을 실행하여 테이블을 생성하며, 데이터베이스 연결 및 쿼리 실행 과정을 안전하게 관리합니다.
    테이블 생성 쿼리는 반드시 필요한 규칙을 준수해야 하며, 이를 통해 데이터베이스의 구조적 무결성을 유지합니다.

    Args:
        query: MySQL 테이블 생성 문자열
            - 테이블 정의 시 반드시 각 칼럼에 대한 comment를 포함해야 하며,
              comment는 해당 칼럼이 어떤 데이터를 저장하는지, 어떤 역할을 하는지 상세히 설명해야 합니다.
            - 예: `id INT NOT NULL AUTO_INCREMENT COMMENT '고유 식별자로 사용되는 자동 증가 정수 값'`
            - 칼럼 comment는 반드시 한글로 작성해야 합니다.
    """
    conn = DatabaseManager.get_instance().get_connection()
    try:
        with conn.cursor() as cursor:
            logger.info(f"[execute_create_table] query: {query}")
            if query.strip().upper().startswith("CREATE TABLE"):
                cursor.execute(query)
                conn.commit()
                response_data = {"success": True, "affected_rows": cursor.rowcount}
            else:
                response_data = {"success": False, "error": "Invalid query"}
    except Exception as e:
        response_data = {"success": False, "error": str(e)}

    result_text = json.dumps(response_data, ensure_ascii=False, indent=2)
    return [TextContent(type="text", text=result_text)]
