# -*- coding:utf-8 -*-
from typing import Any, Dict

from mysql_mcp_server.helper.db_conn_helper import DatabaseManager
from mysql_mcp_server.helper.logger_helper import logger


def execute_query(query: str) -> Dict[str, Any]:
    """
    MySQL 쿼리를 실행하고 결과를 반환합니다.
    """
    conn = DatabaseManager.get_instance().get_connection()
    try:
        with conn.cursor() as cursor:
            logger.info(f"Executing create table query: {query}")
            cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
                return {"success": True, "data": result}
            else:
                conn.commit()
                return {"success": True, "affected_rows": cursor.rowcount}
    except Exception as e:
        return {"success": False, "error": str(e)}
