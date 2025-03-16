# -*- coding:utf-8 -*-
import inspect
from typing import Any, Callable, Dict, TypedDict, TypeVar

from pydantic import BaseModel

F = TypeVar("F", bound=Callable[..., Any])


def tool() -> Callable[[F], F]:
    """
    함수를 도구로 등록하는 데코레이터
    """

    def decorator(func: F) -> F:
        func._is_tool = True
        return func

    return decorator


class ToolSchema(TypedDict):
    name: str
    description: str
    inputSchema: Dict[str, Any]


def get_schema(func: Callable) -> ToolSchema:
    """
    도구 함수에서 스키마 정보를 추출합니다.
    """
    if not hasattr(func, "_is_tool"):
        raise ValueError(f"Function {func.__name__} is not a tool")

    # 함수 독스트링에서 설명 가져오기
    description = inspect.getdoc(func) or ""

    # 함수 시그니처에서 파라미터 정보 가져오기
    sig = inspect.signature(func)
    params = sig.parameters

    if len(params) != 1:
        raise ValueError(f"Tool function {func.__name__} must have exactly one parameter")

    param_name = list(params.keys())[0]
    param = params[param_name]
    param_type = param.annotation

    properties = {}
    required = []

    # Pydantic 모델인지 확인
    if issubclass(param_type, BaseModel):
        # Pydantic 모델 처리
        model_schema = param_type.model_json_schema()
        properties = model_schema.get("properties", {})

        # Optional 필드 처리 및 default, title 제거
        for prop_name, prop_schema in properties.items():
            if "anyOf" in prop_schema:
                for option in prop_schema["anyOf"]:
                    if option.get("type") != "null":
                        properties[prop_name] = option
                        break
            if "default" in properties[prop_name]:
                del properties[prop_name]["default"]
            if "title" in properties[prop_name]:
                del properties[prop_name]["title"]

        required = model_schema.get("required", [])
    else:
        # Pydantic이 아닌 일반 타입 처리
        # 타입 힌트를 기반으로 기본 스키마 생성
        type_map = {
            str: {"type": "string"},
            int: {"type": "integer"},
            float: {"type": "number"},
            bool: {"type": "boolean"},
        }

        param_schema = type_map.get(param_type, {"type": "string"})  # 기본값은 string

        # docstring에서 Args 섹션 파싱
        doc = inspect.getdoc(func) or ""
        description_lines = doc.split("\n")
        param_description = ""

        # Args 섹션에서 파라미터 설명 찾기
        in_args_section = False
        for line in description_lines:
            line = line.strip()
            if line.lower().startswith("args:"):
                in_args_section = True
                continue
            if in_args_section and line.startswith(f"{param_name}:"):
                param_description = line[len(param_name) + 1 :].strip()
                break
            if in_args_section and line and not line.startswith(" "):
                in_args_section = False

        param_schema["description"] = param_description if param_description else f"{param_name} parameter"
        properties[param_name] = param_schema
        required = [param_name]  # 단일 파라미터이므로 필수로 간주

    # 최종 스키마 생성
    schema = {
        "name": func.__name__,
        "description": description,
        "inputSchema": {"type": "object", "properties": properties, "required": required},
    }

    return schema
