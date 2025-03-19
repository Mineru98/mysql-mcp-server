# -*- coding:utf-8 -*-
import json
from typing import List

from mcp.types import TextContent

from mysql_mcp_server.helper.db_conn_helper import DatabaseManager
from mysql_mcp_server.helper.logger_helper import logger
from mysql_mcp_server.helper.tool_decorator import tool


@tool()
def execute_insight_starter(query: str) -> List[TextContent]:
    """
    데이터베이스 테이블의 스키마 정보를 조회하여 데이터 분석에 적합한 쿼리 작성을 지원하는 함수입니다.
    'DESC {table_name}' 형식의 쿼리를 입력하면, 지정된 테이블의 컬럼 이름, 데이터 타입, NULL 여부, 기본값, 코멘트를 포함한 메타데이터를 반환합니다.
    이를 통해 사용자는 데이터베이스 내 테이블 구조를 파악하고, 원하는 분석 목적에 맞는 SQL 쿼리를 설계할 수 있습니다.
    지원되지 않는 쿼리 형식의 경우 오류 메시지를 반환합니다.

    Args:
        query: 데이터베이스에 실행할 SQL 쿼리 문자열. 'DESC {table_name}' 형식을 사용하면 해당 테이블의 스키마 정보를 조회합니다.
               예: 'DESC users' (users 테이블의 구조 반환). 그 외 형식은 현재 지원되지 않습니다.

    Returns:
        List[TextContent]: 조회된 테이블 스키마 정보 또는 오류 메시지를 JSON 형식의 문자열로 포함한 TextContent 리스트.
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
