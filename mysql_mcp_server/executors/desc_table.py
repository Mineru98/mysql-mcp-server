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
    'DESC {table_name}' 형식의 쿼리를 처리할 경우, 테이블의 컬럼 이름, 데이터 타입, NULL 여부, 기본값, 코멘트를 포함한 정보를 반환합니다.
    그 외의 쿼리는 일반 실행 결과를 처리합니다. 결과는 JSON 형식의 문자열로 변환되어 반환됩니다.

    Args:
        query: 데이터베이스에 실행할 SQL 쿼리 문자열. 'DESC {table_name}' 형식이면 테이블의 상세 구조를 조회하며,
               그 외의 경우 쿼리 실행 결과를 처리합니다.
    """
    conn = DatabaseManager.get_instance().get_connection()
    try:
        with conn.cursor() as cursor:
            logger.info(f"[execute_desc_table] query: {query}")
            query_upper = query.strip().upper()
            if query_upper.startswith("DESC"):
                table_name = query.split()[1].strip(";")
                desc_query = """
                    SELECT 
                        COLUMN_NAME AS 'column_name',
                        COLUMN_TYPE AS 'data_type',
                        IS_NULLABLE AS 'is_nullable',
                        COLUMN_DEFAULT AS 'default_value',
                        COLUMN_COMMENT AS 'comment'
                    FROM 
                        INFORMATION_SCHEMA.COLUMNS
                    WHERE 
                        TABLE_NAME = %s
                        AND TABLE_SCHEMA = DATABASE()
                    ORDER BY 
                        ORDINAL_POSITION
                """
                cursor.execute(desc_query, (table_name,))
                result = cursor.fetchall()
                response_data = {"success": True, "data": result}
            else:
                response_data = {"success": False, "error": "Invalid query"}

    except Exception as e:
        response_data = {"success": False, "error": str(e)}

    result_text = json.dumps(response_data, ensure_ascii=False, indent=2)
    return [TextContent(type="text", text=result_text)]
