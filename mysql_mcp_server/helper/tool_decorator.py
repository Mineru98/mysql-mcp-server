# -*- coding:utf-8 -*-
import inspect
from typing import Any, Callable, Dict, List, TypedDict, TypeVar, Union, get_args, get_origin

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

    # 함수 독스트링에서 설명 가져오기 - Args나 Return 부분 제외
    doc = inspect.getdoc(func) or ""
    description_lines = []

    for line in doc.split("\n"):
        line = line.strip()
        # Args, Returns, Examples 등의 섹션 시작을 감지하면 중단
        if line.lower().startswith(("args:", "returns:", "return:", "examples:", "example:")):
            break
        description_lines.append(line)

    # 설명 부분만 추출
    description = "\n".join(description_lines).strip()

    # 함수 시그니처에서 파라미터 정보 가져오기
    sig = inspect.signature(func)
    params = sig.parameters

    # 파라미터가 하나 이상 있는지 확인
    if not params:
        raise ValueError(f"Tool function {func.__name__} must have at least one parameter")

    properties = {}
    required = []

    # 기본 타입 매핑
    type_map = {str: {"type": "string"}, int: {"type": "integer"}, float: {"type": "number"}, bool: {"type": "boolean"}}

    # 각 파라미터에 대해 처리
    for param_name, param in params.items():
        param_type = param.annotation

        # 기본값이 없는 매개변수는 필수로 간주
        if param.default == inspect.Parameter.empty:
            required.append(param_name)

        # Optional 및 List 타입 처리
        origin = get_origin(param_type)
        args = get_args(param_type)

        # 초기화: 기본적으로 필수 파라미터로 설정
        is_optional = False

        if origin is list or origin is List:
            # List 타입 처리
            item_type = args[0] if args else Any
            item_schema = type_map.get(item_type, {"type": "string"})
            param_schema = {"type": "array", "items": item_schema}
        elif origin is Union:
            # Union 타입 처리 (Optional[Type]은 Union[Type, None]으로 변환됨)
            # None이 args에 있는지 확인하여 Optional 여부 판단
            if type(None) in args:
                is_optional = True
                # None이 아닌 타입을 찾음
                for arg in args:
                    if arg is not type(None):
                        non_none_type = arg
                        break
                else:
                    non_none_type = str  # 기본값

                param_schema = type_map.get(non_none_type, {"type": "string"})
            else:
                # 일반 Union 타입 (현재는 단순하게 처리)
                param_schema = {"type": "string"}
        else:
            # 일반 타입 처리
            param_schema = type_map.get(param_type, {"type": "string"})

        # docstring에서 Args 섹션 파싱
        param_description_lines = []
        in_args_section = False
        capturing_description = False

        # Args 섹션에서 파라미터 설명 찾기
        for line in doc.split("\n"):
            line = line.strip()
            if line.lower().startswith("args:"):
                in_args_section = True
                continue
            if in_args_section and not capturing_description and line.startswith(f"{param_name}:"):
                # 파라미터 이름으로 시작하는 줄 발견
                capturing_description = True
                first_line = line[len(param_name) + 1 :].strip()
                if first_line:  # 첫 줄에 설명이 있으면 추가
                    param_description_lines.append(first_line)
                continue
            if capturing_description:
                if (
                    not line
                    or line.lower().startswith(("returns:", "return:", "examples:", "example:"))
                    or (line and not line.startswith((" ", "\t", "-")) and not line.startswith(f"{param_name}:"))
                ):
                    # 들여쓰기 없는 새 섹션 시작 또는 다른 섹션 시작 시 종료
                    capturing_description = False
                    break
                # 들여쓰기된 줄 또는 리스트 항목(-로 시작)이라면 설명의 일부로 간주
                if line:
                    param_description_lines.append(line.strip())

        # 여러 줄을 합쳐서 설명 생성
        param_description = "\n".join(param_description_lines) if param_description_lines else f"{param_name} parameter"
        param_schema["description"] = param_description
        properties[param_name] = param_schema

        # 기본값이 있거나 Optional인 경우 required 목록에서 제외
        if param.default != inspect.Parameter.empty or is_optional:
            if param_name in required:
                required.remove(param_name)

    # 최종 스키마 생성
    schema = {
        "name": func.__name__,
        "description": description,
        "inputSchema": {"type": "object", "properties": properties, "required": required},
    }

    return schema
