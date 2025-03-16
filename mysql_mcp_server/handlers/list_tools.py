# -*- coding:utf-8 -*-
from typing import List

from mcp.types import Tool


async def handle_list_tools() -> List[Tool]:
    """
    MCP에서 'tools/list' 이벤트가 오면,
    우리가 보유한 툴(TOOLS_DEFINITION)을 반환.
    """
    # 순환 임포트 방지를 위해 함수 내부에서 임포트
    from mysql_mcp_server.executors import TOOLS_DEFINITION
    from mysql_mcp_server.helper import get_schema

    tool_objects: List[Tool] = []
    for tdef in TOOLS_DEFINITION:
        tdef = get_schema(tdef)
        tool_objects.append(Tool(name=tdef["name"], description=tdef["description"], inputSchema=tdef["inputSchema"]))
    return tool_objects
