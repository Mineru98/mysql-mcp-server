# MCPMySQLBoilerPlate

### 설치

```
pip install mcp
```

### 실행

```bash
# 모듈 설치
python server.py
```


# MCP Python SDK

<div align="center">

<strong>Python 구현: Model Context Protocol (MCP)</strong>

[![PyPI][pypi-badge]][pypi-url]
[![MIT 라이센스][mit-badge]][mit-url]
[![Python 버전][python-badge]][python-url]
[![문서][docs-badge]][docs-url]
[![사양][spec-badge]][spec-url]
[![GitHub 토론][discussions-badge]][discussions-url]

</div>

<!-- 목차 생략 -->
## 목차

- [개요](#overview)
- [설치](#installation)
- [빠른 시작](#quickstart)
- [MCP란?](#what-is-mcp)
- [핵심 개념](#core-concepts)
  - [서버](#server)
  - [리소스](#resources)
  - [도구](#tools)
  - [프롬프트](#prompts)
  - [이미지](#images)
  - [컨텍스트](#context)
- [서버 실행](#running-your-server)
  - [개발 모드](#development-mode)
  - [Claude 데스크탑 통합](#claude-desktop-integration)
  - [직접 실행](#direct-execution)
- [예시](#examples)
  - [에코 서버](#echo-server)
  - [SQLite 탐색기](#sqlite-explorer)
- [고급 사용법](#advanced-usage)
  - [저수준 서버](#low-level-server)
  - [MCP 클라이언트 작성](#writing-mcp-clients)
  - [MCP 원시값](#mcp-primitives)
  - [서버 기능](#server-capabilities)
- [문서](#documentation)
- [기여](#contributing)
- [라이센스](#license)

[pypi-badge]: https://img.shields.io/pypi/v/mcp.svg
[pypi-url]: https://pypi.org/project/mcp/
[mit-badge]: https://img.shields.io/pypi/l/mcp.svg
[mit-url]: https://github.com/modelcontextprotocol/python-sdk/blob/main/LICENSE
[python-badge]: https://img.shields.io/pypi/pyversions/mcp.svg
[python-url]: https://www.python.org/downloads/
[docs-badge]: https://img.shields.io/badge/docs-modelcontextprotocol.io-blue.svg
[docs-url]: https://modelcontextprotocol.io
[spec-badge]: https://img.shields.io/badge/spec-spec.modelcontextprotocol.io-blue.svg
[spec-url]: https://spec.modelcontextprotocol.io
[discussions-badge]: https://img.shields.io/github/discussions/modelcontextprotocol/python-sdk
[discussions-url]: https://github.com/modelcontextprotocol/python-sdk/discussions

## 개요

Model Context Protocol은 애플리케이션이 LLM에 대해 표준화된 방식으로 컨텍스트를 제공할 수 있게 해주며, 실제 LLM 상호작용과 컨텍스트 제공의 문제를 분리합니다. 이 Python SDK는 MCP 사양을 완벽하게 구현하여, 다음을 쉽게 할 수 있게 합니다:

- 모든 MCP 서버에 연결할 수 있는 MCP 클라이언트 구축
- 리소스, 프롬프트 및 도구를 제공하는 MCP 서버 생성
- 표준 전송 방법인 stdio와 SSE 사용
- 모든 MCP 프로토콜 메시지 및 생애 주기 이벤트 처리

## 설치

## 빠른 시작

계산기 도구와 데이터를 제공하는 간단한 MCP 서버를 만들어 보겠습니다:

```python
# server.py
from mcp.server.fastmcp import FastMCP

# MCP 서버 생성
mcp = FastMCP("Demo")


# 덧셈 도구 추가
@mcp.tool()
def add(a: int, b: int) -> int:
    """두 숫자 더하기"""
    return a + b


# 동적 인사 리소스 추가
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """개인화된 인사말 가져오기"""
    return f"안녕하세요, {name}!"
```

## MCP란?

[Model Context Protocol (MCP)](https://modelcontextprotocol.io)는 LLM 애플리케이션에 대해 데이터를 제공하고 기능을 실행하는 서버를 구축할 수 있게 해줍니다. 이를 웹 API처럼 생각할 수 있지만, 특히 LLM 상호작용을 위해 설계되었습니다. MCP 서버는 다음을 할 수 있습니다:

- **리소스**를 통해 데이터를 제공 (REST API의 GET 엔드포인트와 유사; LLM의 컨텍스트에 정보를 로드하는 데 사용됨)
- **도구**를 통해 기능을 제공 (POST 엔드포인트와 유사; 코드를 실행하거나 부수 효과를 생성하는 데 사용됨)
- **프롬프트**를 통해 상호작용 패턴 정의 (LLM 상호작용을 위한 재사용 가능한 템플릿)
- 그 외에도 다양한 기능

## 핵심 개념

### 서버

FastMCP 서버는 MCP 프로토콜에 대한 핵심 인터페이스입니다. 이 서버는 연결 관리, 프로토콜 준수 및 메시지 라우팅을 처리합니다:

```python
# 시작/종료를 위한 수명 지원 추가
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

from fake_database import Database  # 실제 DB 타입으로 교체

from mcp.server.fastmcp import Context, FastMCP

# 이름이 지정된 서버 생성
mcp = FastMCP("My App")

# 배포 및 개발을 위한 의존성 지정
mcp = FastMCP("My App", dependencies=["pandas", "numpy"])


@dataclass
class AppContext:
    db: Database


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """타입 안전한 컨텍스트로 애플리케이션 생애 주기 관리"""
    # 시작 시 초기화
    db = await Database.connect()
    try:
        yield AppContext(db=db)
    finally:
        # 종료 시 정리
        await db.disconnect()


# 서버에 수명 전달
mcp = FastMCP("My App", lifespan=app_lifespan)


# 도구에서 타입 안전한 수명 컨텍스트 접근
@mcp.tool()
def query_db(ctx: Context) -> str:
    """초기화된 리소스를 사용하는 도구"""
    db = ctx.request_context.lifespan_context["db"]
    return db.query()
```

### 리소스

리소스는 LLM에 데이터를 제공하는 방법입니다. 이는 REST API의 GET 엔드포인트와 유사하며, 데이터를 제공하지만 중요한 계산을 수행하거나 부수 효과를 일으키지 않습니다:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")


@mcp.resource("config://app")
def get_config() -> str:
    """정적 구성 데이터"""
    return "앱 구성 여기"


@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """동적 사용자 데이터"""
    return f"사용자 {user_id}의 프로필 데이터"
```

### 도구

도구는 LLM이 서버를 통해 작업을 수행할 수 있게 합니다. 리소스와 달리 도구는 계산을 수행하고 부수 효과를 일으킬 것으로 기대됩니다:

```python
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")


@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """체중(kg)과 신장(m)을 기준으로 BMI 계산"""
    return weight_kg / (height_m**2)


@mcp.tool()
async def fetch_weather(city: str) -> str:
    """도시의 현재 날씨 가져오기"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weather.com/{city}")
        return response.text
```

### 프롬프트

프롬프트는 LLM이 서버와 효과적으로 상호작용할 수 있도록 도와주는 재사용 가능한 템플릿입니다:

```python
from mcp.server.fastmcp import FastMCP, types

mcp = FastMCP("My App")


@mcp.prompt()
def review_code(code: str) -> str:
    return f"다음 코드를 검토해주세요:\n\n{code}"


@mcp.prompt()
def debug_error(error: str) -> list[types.Message]:
    return [
        types.UserMessage("이 오류가 발생했어요:"),
        types.UserMessage(error),
        types.AssistantMessage("도움을 드릴게요. 지금까지 무엇을 시도해보셨나요?"),
    ]
```

### 이미지

FastMCP는 자동으로 이미지 데이터를 처리하는 `Image` 클래스를 제공합니다:

```python
from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage

mcp = FastMCP("My App")


@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """이미지에서 썸네일 만들기"""
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")
```

### 컨텍스트

`Context` 객체는 도구와 리소스가 MCP 기능에 접근할 수 있게 해줍니다:

```python
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("My App")


@mcp.tool()
async def long_task(files: list[str], ctx: Context) -> str:
    """파일 여러 개를 처리하며 진행 상황 추적"""
    for i, file in enumerate(files):
        ctx.info(f"{file} 처리 중")
        await ctx.report_progress(i, len(files))
        data, mime_type = await ctx.read_resource(f"file://{file}")
    return "처리 완료"
```

## 서버 실행

### 개발 모드

서버를 빠르게 테스트하고 디버깅하는 가장 좋은 방법은 MCP 검사기를 사용하는 것입니다:

```bash
mcp dev server.py

# 의존성 추가
mcp dev server.py --with pandas --with numpy

# 로컬 코드 마운트
mcp dev server.py --with-editable .
```

### Claude 데스크탑 통합

서버가 준비되면, Claude 데스크탑에 설치할 수 있습니다:

```bash
mcp install server.py

# 사용자 지정 이름
mcp install server.py --name "My Analytics Server"

# 환경 변수
mcp install server.py -v API_KEY=abc123 -v DB_URL=postgres://...
mcp install server.py -f .env
```

### 직접 실행

고급 배포 시나리오에서는 직접 실행할 수 있습니다:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")

if __name__ == "__main__":
    mcp.run()
```

실행하려면:
```bash
python server.py
# 또는
mcp run server.py
```

## 예시

### 에코 서버

리소스, 도구, 프롬프트를 사용하는 간단한 서버:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Echo")


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """메시지를 리소스로 에코"""
    return f"리소스 에코: {message}"


@mcp.tool()
def echo_tool(message: str) -> str:
    """메시지를 도구로 에코"""
    return f"도구 에코: {message}"


@mcp.prompt()
def echo_prompt(message: str) -> str:
    """에코 프롬프트 생성"""
    return f"이 메시지를 처리해주세요: {message}"
```

### SQLite 탐색기

데이터베이스 통합을 보여주는 복잡한 예시:

```python
import sqlite3

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SQLite Explorer")


@mcp.resource("schema://main")
def get_schema() -> str:
    """데이터베이스 스키마를 리소스로 제공"""
    conn = sqlite3.connect("database.db")
    schema = conn.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
    return "\n".join(sql[0] for sql in schema if sql[0])


@mcp.tool()
def query_data(sql: str) -> str:
    """안전하게 SQL 쿼리 실행"""
    conn = sqlite3.connect("database.db")
    try:
        result = conn.execute(sql).fetchall()
        return "\n".join(str(row) for row in result)
    except Exception as e:
        return f"오류: {str(e)}"
```

## 고급 사용법

### 저수준 서버

더 많은 제어를 위해 저수준 서버 구현을 직접 사용할 수 있습니다. 이는 프로토콜에 대한 완전한 접근을 제공하고 서버의 모든 측면을 사용자 지정할 수 있게 해줍니다. 수명 관리 API를 통해서도 이를 처리할 수 있습니다:

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fake_database import Database  # 실제 DB 타입으로 교체

from mcp.server import Server


@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[dict]:
    """서버 시작 및 종료 생애 주기 관리."""
    # 시작 시 리소스 초기화
    db = await Database.connect()
    try:
        yield {"db": db}
    finally:
        # 종료 시 정리
        await db.disconnect()


# 수명 API를 서버에 전달
server = Server("example-server", lifespan=server_lifespan)


# 핸들러에서 수명 컨텍스트 접근
@server.call_tool()
async def query_db(name: str, arguments: dict) -> list:
    ctx = server.request_context
    db = ctx.lifespan_context["db"]
    return await db.query(arguments["query"])
```

수명 API는 다음을 제공합니다:
- 서버가 시작할 때 리소스를 초기화하고 종료할 때 이를 정리하는 방법
- 핸들러에서 요청 컨텍스트를 통해 초기화된 리소스에 접근할 수 있는 방법
- 수명과 요청 핸들러 간에 타입 안전한 컨텍스트 전달

```python
import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# 서버 인스턴스 생성
server = Server("example-server")


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="example-prompt",
            description="예시 프롬프트 템플릿",
            arguments=[
                types.PromptArgument(
                    name="arg1", description="예시 인수", required=True
                )
            ],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    if name != "example-prompt":
        raise ValueError(f"알 수 없는 프롬프트: {name}")

    return types.GetPromptResult(
        description="예시 프롬프트",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text="예시 프롬프트 텍스트"),
            )
        ],
    )


async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
```

### MCP 클라이언트 작성

SDK는 MCP 서버에 연결할 수 있는 고수준 클라이언트 인터페이스를 제공합니다:

```python
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# stdio 연결을 위한 서버 파라미터 생성
server_params = StdioServerParameters(
    command="python",  # 실행 파일
    args=["example_server.py"],  # 선택적 명령줄 인수
    env=None,  # 선택적 환경 변수
)


# 선택적: 샘플링 콜백 생성
async def handle_sampling_message(
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, sampling_callback=handle_sampling_message
        ) as session:
            # 연결 초기화
            await session.initialize()

            # 사용 가능한 프롬프트 나열
            prompts = await session.list_prompts()

            # 프롬프트 가져오기
            prompt = await session.get_prompt(
                "example-prompt", arguments={"arg1": "value"}
            )

            # 사용 가능한 리소스 나열
            resources = await session.list_resources()

            # 사용 가능한 도구 나열
            tools = await session.list_tools()



            # 리소스 읽기
            content, mime_type = await session.read_resource("file://some/path")

            # 도구 호출
            result = await session.call_tool("tool-name", arguments={"arg1": "value"})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
```

### MCP 원시값

MCP 프로토콜은 서버가 구현할 수 있는 세 가지 핵심 원시값을 정의합니다:

| 원시값     | 제어                | 설명                                               | 예시 사용                         |
|-----------|--------------------|---------------------------------------------------|-----------------------------------|
| 프롬프트   | 사용자 제어        | 사용자가 선택한 대로 상호작용하는 템플릿          | 슬래시 명령, 메뉴 옵션            |
| 리소스     | 애플리케이션 제어   | 클라이언트 애플리케이션이 관리하는 컨텍스트 데이터 | 파일 내용, API 응답               |
| 도구       | 모델 제어           | LLM이 작업을 수행하도록 서버에 의해 노출된 함수   | API 호출, 데이터 업데이트         |

### 서버 기능

MCP 서버는 초기화 시 기능을 선언합니다:

| 기능       | 기능 플래그                | 설명                          |
|------------|--------------------------|-------------------------------|
| `프롬프트` | `listChanged`             | 프롬프트 템플릿 관리           |
| `리소스`   | `subscribe`<br/>`listChanged`| 리소스 노출 및 업데이트        |
| `도구`     | `listChanged`             | 도구 검색 및 실행              |
| `로깅`     | -                        | 서버 로깅 설정                |
| `완료`     | -                        | 인수 자동 완성 제안           |

## 문서

- [Model Context Protocol 문서](https://modelcontextprotocol.io)
- [Model Context Protocol 사양](https://spec.modelcontextprotocol.io)
- [공식적으로 지원되는 서버들](https://github.com/modelcontextprotocol/servers)