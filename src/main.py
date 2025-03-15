import argparse
import logging
import os
import sys

import pymysql.cursors
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# .env 파일 로드
load_dotenv()

# 명령줄 인자 파싱
parser = argparse.ArgumentParser(description="MySQL MCP 서버 실행")
parser.add_argument("--mcp-port", type=int, help="MCP 서버 포트 번호")
parser.add_argument("--mysql-host", type=str, help="MySQL 서버 호스트")
parser.add_argument("--mysql-port", type=int, help="MySQL 서버 포트 번호")
parser.add_argument("--mysql-user", type=str, help="MySQL 서버 사용자 이름")
parser.add_argument("--mysql-password", type=str, help="MySQL 서버 비밀번호")
parser.add_argument("--mysql-database", type=str, help="MySQL 서버 데이터베이스 이름")
args = parser.parse_args()

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("mysql-mcp-server")

# 포트 설정 (우선순위: 명령줄 인자 > 환경변수 > 기본값)
port = args.mcp_port if args.mcp_port else int(os.getenv("MCP_PORT", 8081))
mysql_host = args.mysql_host if args.mysql_host else os.getenv("MYSQL_HOST", "localhost")
mysql_port = args.mysql_port if args.mysql_port else int(os.getenv("MYSQL_PORT", 3306))
mysql_user = args.mysql_user if args.mysql_user else os.getenv("MYSQL_USER", "root")
mysql_password = args.mysql_password if args.mysql_password else os.getenv("MYSQL_PASSWORD", "mcpTest1234!!!")
mysql_database = args.mysql_database if args.mysql_database else os.getenv("MYSQL_DATABASE", "mcp_test")

logger.info(f"서버가 포트 {port}에서 시작됩니다.")

try:
    conn = pymysql.connect(
        host=mysql_host,
        port=mysql_port,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database,
        cursorclass=pymysql.cursors.DictCursor,
    )
except Exception as e:
    logger.error(f"MySQL 연결 오류: {e}")
    sys.exit(1)

# Create an MCP server
mcp = FastMCP(name="MySQL MCP 서버", debug=True, port=port)


@mcp.tool()
def mysql_query(sql: str) -> str:
    """Run a read-only MySQL query"""
    message = f"실행할 SQL 쿼리: {sql}"
    logger.info(message)  # 로거를 통한 로그 출력
    # 여기에 실제 MySQL 쿼리 실행 로직이 들어가야 합니다
    return f"쿼리 결과: {sql}"


@mcp.tool()
def echo_tool(message: str) -> str:
    """Echo a message as a tool"""
    log_message = f"Tool echo: {message}"
    logger.info(log_message)  # 로거를 통한 로그 출력
    return message


@mcp.prompt()
def echo_prompt(message: str) -> str:
    """Create an echo prompt"""
    log_message = f"Prompt echo: {message}"
    logger.info(log_message)
    return f"Please process this message: {message}"


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    log_message = f"Greeting for: {name}"
    logger.info(log_message)
    return f"Hello, {name}!"


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    log_message = f"Resource echo: {message}"
    logger.info(log_message)
    return f"Resource echo: {message}"


if __name__ == "__main__":
    logger.info("Starting MCP server...")
    mcp.run(transport="sse")
