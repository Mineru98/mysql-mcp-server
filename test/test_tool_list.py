# -*- coding:utf-8 -*-
import os
import sys
import unittest
from typing import Literal

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mysql_mcp_server.helper.tool_decorator import get_schema, tool


@tool()
def test_tool(query: Literal["a", "b", "c"]) -> int:
    """
    test_tool 도구는 주어진 쿼리를 반환합니다.

    Args:
        query: 쿼리 문자열
        - 가능한 값: "a", "b", "c"


    """
    return query


class TestToolList(unittest.TestCase):
    def test_get_schema(self):
        schema = get_schema(test_tool)
        assert schema["name"] == "test_tool"
        assert schema["description"] == "test_tool 도구는 주어진 쿼리를 반환합니다."
        assert schema["inputSchema"] == {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "enum": ["a", "b", "c"],
                    "description": '쿼리 문자열\n- 가능한 값: "a", "b", "c"',
                }
            },
            "required": ["query"],
        }


if __name__ == "__main__":
    unittest.main()
