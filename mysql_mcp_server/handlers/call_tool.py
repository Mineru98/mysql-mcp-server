# -*- coding:utf-8 -*-
import asyncio
from typing import Any, Dict, List

from mcp.types import TextContent

from mysql_mcp_server.excutors import execute_create_table, execute_select_query, execute_show_table
from mysql_mcp_server.models import MysqlCreateTableInput, MysqlQueryInput, MysqlShowTableInput


async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """
    MCP에서 'tool/call' 이벤트로 특정 툴(name)을 호출하면,
    여기서 그 이름에 맞게 실제 비즈니스 로직(call_chat_api 등)을 실행.

    반환값은 List[TextContent] 형태여야 하며, MCP에 문자열 형태로 전달된다.
    """
    try:
        if name == "execute_select_query":
            input_arguments = MysqlQueryInput(query=arguments.get("query", "").strip())

            response_data = await asyncio.to_thread(execute_select_query, query=input_arguments.query)
            return [response_data]
        elif name == "execute_create_table":
            input_arguments = MysqlCreateTableInput(query=arguments.get("query", "").strip())

            response_data = await asyncio.to_thread(execute_create_table, query=input_arguments.query)
            return [response_data]
        elif name == "execute_show_table":
            input_arguments = MysqlShowTableInput(query=arguments.get("query", "").strip())

            response_data = await asyncio.to_thread(execute_show_table, query=input_arguments.query)
            return [response_data]
        else:
            raise ValueError(f"Tool '{name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Tool call error: {str(e)}") from e
