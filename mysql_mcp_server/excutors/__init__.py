# -*- coding:utf-8 -*-
import inspect
import sys

from .create_table import execute_create_table
from .select_query import execute_select_query
from .show_table import execute_show_table

__all__ = ["execute_create_table", "execute_select_query", "execute_show_table"]

TOOLS_DEFINITION = [
    obj
    for name, obj in inspect.getmembers(sys.modules[__name__])
    if inspect.isfunction(obj) and hasattr(obj, "_is_tool") and obj._is_tool
]
