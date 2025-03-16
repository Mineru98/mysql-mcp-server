# -*- coding:utf-8 -*-
from pydantic import BaseModel, Field


class MysqlQueryInput(BaseModel):
    query: str = Field(description="MySQL 쿼리 문자열")


class MysqlCreateTableInput(BaseModel):
    query: str = Field(description="MySQL 테이블 생성 문자열")


class MysqlShowTableInput(BaseModel):
    query: str = Field(description="MySQL 테이블 조회 문자열")
