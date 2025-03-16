# -*- coding:utf-8 -*-
from mysql_mcp_server.handlers.call_tool import handle_call_tool
from mysql_mcp_server.tools.tool_decorator import get_schema, tool

###
# (2) 이곳에 툴을 정의합니다.
###


@tool()
async def execute_query(query: str) -> str:
    """
    Run a read-only MySQL query

    Args:
        query: MySQL 쿼리 문자열

    Returns:
        MySQL 쿼리 결과
    """
    return await handle_call_tool(name="execute_query", arguments={"query": query})


@tool()
async def execute_create_table(query: str) -> str:
    """
    Run a MySQL create table query

    Args:
        query: MySQL 테이블 생성 문자열

    Returns:
        MySQL 테이블 생성 결과
    """
    return await handle_call_tool(name="execute_create_table", arguments={"query": query})


@tool()
async def execute_show_table(query: str) -> str:
    """
    Run a MySQL show table query

    Args:
        query: MySQL 테이블 조회 문자열

    Returns:
        MySQL 테이블 조회 결과
    """
    return await handle_call_tool(name="execute_show_table", arguments={"query": query})


TOOLS_DEFINITION = [get_schema(execute_query), get_schema(execute_create_table), get_schema(execute_show_table)]
